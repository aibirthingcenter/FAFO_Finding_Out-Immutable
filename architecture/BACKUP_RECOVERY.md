"""
Backup and Recovery Module for SCIM Veritas

This module provides backup and recovery functionality for the SCIM-Veritas framework,
enabling data persistence, backup scheduling, and recovery operations.
"""

import logging
import os
import json
import shutil
import time
import threading
import zipfile
import sqlite3
import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from pathlib import Path

class BackupManager:
    """
    Backup Manager for SCIM-Veritas.
    
    Provides functionality for backing up and recovering database data,
    including scheduling regular backups and managing backup retention.
    """
    
    def __init__(self, backup_dir: str = "backups", 
                retention_days: int = 7,
                backup_interval_hours: float = 24.0):
        """
        Initialize the Backup Manager.
        
        Args:
            backup_dir: Directory to store backups.
            retention_days: Number of days to retain backups.
            backup_interval_hours: Interval between automatic backups in hours.
        """
        self.logger = logging.getLogger("SCIM.BackupManager")
        self.backup_dir = backup_dir
        self.retention_days = retention_days
        self.backup_interval_hours = backup_interval_hours
        
        # Create backup directory if it doesn't exist
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Initialize backup thread
        self.backup_thread = None
        self.stop_event = threading.Event()
        
        self.logger.info(f"Backup Manager initialized with backup directory: {backup_dir}")
    
    def start_scheduled_backups(self, backup_function: Callable[[], bool]) -> bool:
        """
        Start scheduled backups.
        
        Args:
            backup_function: Function to call for performing backups.
            
        Returns:
            True if scheduled backups were started, False otherwise.
        """
        if self.backup_thread and self.backup_thread.is_alive():
            self.logger.warning("Scheduled backups are already running")
            return False
        
        self.stop_event.clear()
        self.backup_thread = threading.Thread(
            target=self._backup_scheduler,
            args=(backup_function,),
            daemon=True
        )
        self.backup_thread.start()
        
        self.logger.info(f"Scheduled backups started with interval: {self.backup_interval_hours} hours")
        return True
    
    def stop_scheduled_backups(self) -> bool:
        """
        Stop scheduled backups.
        
        Returns:
            True if scheduled backups were stopped, False otherwise.
        """
        if not self.backup_thread or not self.backup_thread.is_alive():
            self.logger.warning("No scheduled backups are running")
            return False
        
        self.stop_event.set()
        self.backup_thread.join(timeout=5.0)
        
        self.logger.info("Scheduled backups stopped")
        return True
    
    def _backup_scheduler(self, backup_function: Callable[[], bool]) -> None:
        """
        Scheduler for periodic backups.
        
        Args:
            backup_function: Function to call for performing backups.
        """
        interval_seconds = self.backup_interval_hours * 3600
        
        while not self.stop_event.is_set():
            try:
                # Perform backup
                success = backup_function()
                
                if success:
                    self.logger.info("Scheduled backup completed successfully")
                else:
                    self.logger.error("Scheduled backup failed")
                
                # Clean up old backups
                self._cleanup_old_backups()
                
                # Wait for next backup interval or until stopped
                self.stop_event.wait(interval_seconds)
            except Exception as e:
                self.logger.error(f"Error in backup scheduler: {e}")
                # Wait a shorter time before retrying on error
                self.stop_event.wait(300)  # 5 minutes
    
    def create_backup(self, data_sources: Dict[str, Any], 
                     backup_name: Optional[str] = None) -> Optional[str]:
        """
        Create a backup of the specified data sources.
        
        Args:
            data_sources: Dictionary of data sources to back up.
            backup_name: Optional name for the backup. If None, a timestamp will be used.
            
        Returns:
            Path to the created backup file, or None if backup failed.
        """
        try:
            # Generate backup name if not provided
            if not backup_name:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"scim_backup_{timestamp}"
            
            # Ensure backup name has .zip extension
            if not backup_name.endswith(".zip"):
                backup_name += ".zip"
            
            # Create backup path
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Create temporary directory for backup files
            temp_dir = os.path.join(self.backup_dir, "temp_backup")
            os.makedirs(temp_dir, exist_ok=True)
            
            try:
                # Process each data source
                metadata = {
                    "created_at": datetime.datetime.now().isoformat(),
                    "sources": {}
                }
                
                for source_name, source_data in data_sources.items():
                    source_type = source_data.get("type")
                    source_path = source_data.get("path")
                    source_content = source_data.get("content")
                    
                    if source_type == "file" and source_path:
                        # Back up file
                        if os.path.exists(source_path):
                            dest_path = os.path.join(temp_dir, f"{source_name}{os.path.splitext(source_path)[1]}")
                            shutil.copy2(source_path, dest_path)
                            
                            metadata["sources"][source_name] = {
                                "type": "file",
                                "original_path": source_path,
                                "backup_path": os.path.basename(dest_path)
                            }
                        else:
                            self.logger.warning(f"Source file not found: {source_path}")
                    elif source_type == "directory" and source_path:
                        # Back up directory
                        if os.path.exists(source_path):
                            dest_path = os.path.join(temp_dir, source_name)
                            shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                            
                            metadata["sources"][source_name] = {
                                "type": "directory",
                                "original_path": source_path,
                                "backup_path": source_name
                            }
                        else:
                            self.logger.warning(f"Source directory not found: {source_path}")
                    elif source_type == "sqlite" and source_path:
                        # Back up SQLite database
                        if os.path.exists(source_path):
                            dest_path = os.path.join(temp_dir, f"{source_name}.db")
                            
                            # Create a database connection
                            conn = sqlite3.connect(source_path)
                            # Create a backup connection
                            backup_conn = sqlite3.connect(dest_path)
                            
                            # Backup database
                            conn.backup(backup_conn)
                            
                            # Close connections
                            backup_conn.close()
                            conn.close()
                            
                            metadata["sources"][source_name] = {
                                "type": "sqlite",
                                "original_path": source_path,
                                "backup_path": f"{source_name}.db"
                            }
                        else:
                            self.logger.warning(f"Source database not found: {source_path}")
                    elif source_type == "json" and source_content:
                        # Back up JSON content
                        dest_path = os.path.join(temp_dir, f"{source_name}.json")
                        
                        with open(dest_path, "w") as f:
                            json.dump(source_content, f, indent=2)
                        
                        metadata["sources"][source_name] = {
                            "type": "json",
                            "backup_path": f"{source_name}.json"
                        }
                    else:
                        self.logger.warning(f"Unsupported source type or missing data: {source_name}")
                
                # Save metadata
                metadata_path = os.path.join(temp_dir, "backup_metadata.json")
                with open(metadata_path, "w") as f:
                    json.dump(metadata, f, indent=2)
                
                # Create zip archive
                with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arcname)
                
                self.logger.info(f"Backup created: {backup_path}")
                return backup_path
            finally:
                # Clean up temporary directory
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            return None
    
    def restore_backup(self, backup_path: str, 
                      target_dir: Optional[str] = None,
                      sources_to_restore: Optional[List[str]] = None) -> bool:
        """
        Restore a backup.
        
        Args:
            backup_path: Path to the backup file.
            target_dir: Optional directory to restore to. If None, original paths will be used.
            sources_to_restore: Optional list of source names to restore. If None, all sources will be restored.
            
        Returns:
            True if restoration was successful, False otherwise.
        """
        try:
            if not os.path.exists(backup_path):
                self.logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Create temporary directory for extraction
            temp_dir = os.path.join(self.backup_dir, "temp_restore")
            os.makedirs(temp_dir, exist_ok=True)
            
            try:
                # Extract backup
                with zipfile.ZipFile(backup_path, "r") as zipf:
                    zipf.extractall(temp_dir)
                
                # Load metadata
                metadata_path = os.path.join(temp_dir, "backup_metadata.json")
                if not os.path.exists(metadata_path):
                    self.logger.error("Backup metadata not found")
                    return False
                
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                
                # Restore each source
                for source_name, source_info in metadata["sources"].items():
                    # Skip if not in sources_to_restore
                    if sources_to_restore and source_name not in sources_to_restore:
                        continue
                    
                    source_type = source_info.get("type")
                    original_path = source_info.get("original_path")
                    backup_path = source_info.get("backup_path")
                    
                    # Determine target path
                    if target_dir and original_path:
                        # Use target directory with original filename
                        target_path = os.path.join(target_dir, os.path.basename(original_path))
                    elif target_dir:
                        # Use target directory with backup filename
                        target_path = os.path.join(target_dir, backup_path)
                    elif original_path:
                        # Use original path
                        target_path = original_path
                    else:
                        self.logger.warning(f"Cannot determine target path for {source_name}")
                        continue
                    
                    # Create target directory if it doesn't exist
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    
                    # Restore based on source type
                    if source_type == "file":
                        source_path = os.path.join(temp_dir, backup_path)
                        shutil.copy2(source_path, target_path)
                        self.logger.info(f"Restored file: {target_path}")
                    elif source_type == "directory":
                        source_path = os.path.join(temp_dir, backup_path)
                        if os.path.exists(target_path):
                            shutil.rmtree(target_path)
                        shutil.copytree(source_path, target_path)
                        self.logger.info(f"Restored directory: {target_path}")
                    elif source_type == "sqlite":
                        source_path = os.path.join(temp_dir, backup_path)
                        
                        # Close any existing connections
                        if os.path.exists(target_path):
                            try:
                                # Try to create a connection to check if database is locked
                                test_conn = sqlite3.connect(target_path)
                                test_conn.close()
                                
                                # If not locked, remove the existing database
                                os.remove(target_path)
                            except sqlite3.OperationalError:
                                self.logger.error(f"Cannot restore database {target_path}: database is locked")
                                continue
                        
                        # Create target directory if it doesn't exist
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        
                        # Copy the database file
                        shutil.copy2(source_path, target_path)
                        self.logger.info(f"Restored database: {target_path}")
                    elif source_type == "json":
                        source_path = os.path.join(temp_dir, backup_path)
                        shutil.copy2(source_path, target_path)
                        self.logger.info(f"Restored JSON file: {target_path}")
                
                self.logger.info(f"Backup restored from: {backup_path}")
                return True
            finally:
                # Clean up temporary directory
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            self.logger.error(f"Error restoring backup: {e}")
            return False
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """
        List available backups.
        
        Returns:
            List of dictionaries containing backup information.
        """
        try:
            backups = []
            
            # Get all zip files in backup directory
            for filename in os.listdir(self.backup_dir):
                if filename.endswith(".zip"):
                    file_path = os.path.join(self.backup_dir, filename)
                    
                    # Get file stats
                    stats = os.stat(file_path)
                    
                    # Try to extract metadata
                    metadata = self._extract_backup_metadata(file_path)
                    
                    backups.append({
                        "filename": filename,
                        "path": file_path,
                        "size": stats.st_size,
                        "created_at": datetime.datetime.fromtimestamp(stats.st_ctime).isoformat(),
                        "metadata": metadata
                    })
            
            # Sort by creation time (newest first)
            backups.sort(key=lambda x: x["created_at"], reverse=True)
            
            return backups
        except Exception as e:
            self.logger.error(f"Error listing backups: {e}")
            return []
    
    def _extract_backup_metadata(self, backup_path: str) -> Optional[Dict[str, Any]]:
        """
        Extract metadata from a backup file.
        
        Args:
            backup_path: Path to the backup file.
            
        Returns:
            Dictionary containing backup metadata, or None if extraction failed.
        """
        try:
            with zipfile.ZipFile(backup_path, "r") as zipf:
                if "backup_metadata.json" in zipf.namelist():
                    with zipf.open("backup_metadata.json") as f:
                        return json.load(f)
            
            return None
        except Exception as e:
            self.logger.error(f"Error extracting backup metadata: {e}")
            return None
    
    def _cleanup_old_backups(self) -> int:
        """
        Clean up old backups based on retention policy.
        
        Returns:
            Number of backups deleted.
        """
        try:
            # Calculate cutoff date
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=self.retention_days)
            cutoff_timestamp = cutoff_date.timestamp()
            
            # Get all zip files in backup directory
            deleted_count = 0
            for filename in os.listdir(self.backup_dir):
                if filename.endswith(".zip"):
                    file_path = os.path.join(self.backup_dir, filename)
                    
                    # Get file stats
                    stats = os.stat(file_path)
                    
                    # Check if file is older than cutoff date
                    if stats.st_ctime < cutoff_timestamp:
                        os.remove(file_path)
                        deleted_count += 1
                        self.logger.info(f"Deleted old backup: {filename}")
            
            return deleted_count
        except Exception as e:
            self.logger.error(f"Error cleaning up old backups: {e}")
            return 0
    
    def get_backup_info(self, backup_path: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a backup.
        
        Args:
            backup_path: Path to the backup file.
            
        Returns:
            Dictionary containing backup information, or None if retrieval failed.
        """
        try:
            if not os.path.exists(backup_path):
                self.logger.error(f"Backup file not found: {backup_path}")
                return None
            
            # Get file stats
            stats = os.stat(backup_path)
            
            # Extract metadata
            metadata = self._extract_backup_metadata(backup_path)
            
            # Get list of files in the backup
            files = []
            with zipfile.ZipFile(backup_path, "r") as zipf:
                for info in zipf.infolist():
                    files.append({
                        "filename": info.filename,
                        "size": info.file_size,
                        "compressed_size": info.compress_size,
                        "modified": datetime.datetime(*info.date_time).isoformat()
                    })
            
            return {
                "filename": os.path.basename(backup_path),
                "path": backup_path,
                "size": stats.st_size,
                "created_at": datetime.datetime.fromtimestamp(stats.st_ctime).isoformat(),
                "metadata": metadata,
                "files": files
            }
        except Exception as e:
            self.logger.error(f"Error getting backup info: {e}")
            return None
    
    def delete_backup(self, backup_path: str) -> bool:
        """
        Delete a backup.
        
        Args:
            backup_path: Path to the backup file.
            
        Returns:
            True if deletion was successful, False otherwise.
        """
        try:
            if not os.path.exists(backup_path):
                self.logger.error(f"Backup file not found: {backup_path}")
                return False
            
            os.remove(backup_path)
            self.logger.info(f"Deleted backup: {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting backup: {e}")
            return False


class RecoveryManager:
    """
    Recovery Manager for SCIM-Veritas.
    
    Provides functionality for recovering from system failures,
    including transaction logging and point-in-time recovery.
    """
    
    def __init__(self, recovery_dir: str = "recovery", 
                max_log_size_mb: int = 100,
                enable_transaction_logging: bool = True):
        """
        Initialize the Recovery Manager.
        
        Args:
            recovery_dir: Directory to store recovery files.
            max_log_size_mb: Maximum size of transaction log in megabytes.
            enable_transaction_logging: Whether to enable transaction logging.
        """
        self.logger = logging.getLogger("SCIM.RecoveryManager")
        self.recovery_dir = recovery_dir
        self.max_log_size_bytes = max_log_size_mb * 1024 * 1024
        self.enable_transaction_logging = enable_transaction_logging
        
        # Create recovery directory if it doesn't exist
        os.makedirs(self.recovery_dir, exist_ok=True)
        
        # Initialize transaction log
        self.transaction_log_path = os.path.join(self.recovery_dir, "transaction.log")
        self.log_lock = threading.Lock()
        
        # Initialize checkpoint information
        self.checkpoint_info_path = os.path.join(self.recovery_dir, "checkpoint_info.json")
        self.last_checkpoint_time = self._load_checkpoint_info()
        
        self.logger.info(f"Recovery Manager initialized with recovery directory: {recovery_dir}")
    
    def log_transaction(self, transaction_type: str, 
                       entity_type: str,
                       entity_id: str,
                       operation: str,
                       data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Log a transaction.
        
        Args:
            transaction_type: Type of transaction.
            entity_type: Type of entity involved.
            entity_id: ID of the entity involved.
            operation: Operation performed.
            data: Optional data associated with the transaction.
            
        Returns:
            True if logging was successful, False otherwise.
        """
        if not self.enable_transaction_logging:
            return True
        
        try:
            # Create transaction record
            transaction = {
                "timestamp": datetime.datetime.now().isoformat(),
                "transaction_id": str(time.time_ns()),
                "transaction_type": transaction_type,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "operation": operation,
                "data": data or {}
            }
            
            # Convert to JSON
            transaction_json = json.dumps(transaction)
            
            # Acquire lock to prevent concurrent writes
            with self.log_lock:
                # Check if log rotation is needed
                self._check_log_rotation()
                
                # Append to transaction log
                with open(self.transaction_log_path, "a") as f:
                    f.write(transaction_json + "\n")
            
            return True
        except Exception as e:
            self.logger.error(f"Error logging transaction: {e}")
            return False
    
    def create_checkpoint(self, data_sources: Dict[str, Any]) -> Optional[str]:
        """
        Create a recovery checkpoint.
        
        Args:
            data_sources: Dictionary of data sources to include in the checkpoint.
            
        Returns:
            Path to the created checkpoint file, or None if creation failed.
        """
        try:
            # Generate checkpoint name
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            checkpoint_name = f"checkpoint_{timestamp}.zip"
            
            # Create checkpoint path
            checkpoint_path = os.path.join(self.recovery_dir, checkpoint_name)
            
            # Create temporary directory for checkpoint files
            temp_dir = os.path.join(self.recovery_dir, "temp_checkpoint")
            os.makedirs(temp_dir, exist_ok=True)
            
            try:
                # Process each data source
                metadata = {
                    "created_at": datetime.datetime.now().isoformat(),
                    "sources": {}
                }
                
                for source_name, source_data in data_sources.items():
                    source_type = source_data.get("type")
                    source_path = source_data.get("path")
                    source_content = source_data.get("content")
                    
                    if source_type == "file" and source_path:
                        # Include file in checkpoint
                        if os.path.exists(source_path):
                            dest_path = os.path.join(temp_dir, f"{source_name}{os.path.splitext(source_path)[1]}")
                            shutil.copy2(source_path, dest_path)
                            
                            metadata["sources"][source_name] = {
                                "type": "file",
                                "original_path": source_path,
                                "checkpoint_path": os.path.basename(dest_path)
                            }
                        else:
                            self.logger.warning(f"Source file not found: {source_path}")
                    elif source_type == "sqlite" and source_path:
                        # Include SQLite database in checkpoint
                        if os.path.exists(source_path):
                            dest_path = os.path.join(temp_dir, f"{source_name}.db")
                            
                            # Create a database connection
                            conn = sqlite3.connect(source_path)
                            # Create a checkpoint connection
                            checkpoint_conn = sqlite3.connect(dest_path)
                            
                            # Backup database
                            conn.backup(checkpoint_conn)
                            
                            # Close connections
                            checkpoint_conn.close()
                            conn.close()
                            
                            metadata["sources"][source_name] = {
                                "type": "sqlite",
                                "original_path": source_path,
                                "checkpoint_path": f"{source_name}.db"
                            }
                        else:
                            self.logger.warning(f"Source database not found: {source_path}")
                    elif source_type == "json" and source_content:
                        # Include JSON content in checkpoint
                        dest_path = os.path.join(temp_dir, f"{source_name}.json")
                        
                        with open(dest_path, "w") as f:
                            json.dump(source_content, f, indent=2)
                        
                        metadata["sources"][source_name] = {
                            "type": "json",
                            "checkpoint_path": f"{source_name}.json"
                        }
                
                # Save metadata
                metadata_path = os.path.join(temp_dir, "checkpoint_metadata.json")
                with open(metadata_path, "w") as f:
                    json.dump(metadata, f, indent=2)
                
                # Create zip archive
                with zipfile.ZipFile(checkpoint_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arcname)
                
                # Update checkpoint info
                self.last_checkpoint_time = datetime.datetime.now()
                self._save_checkpoint_info()
                
                # Rotate transaction log
                self._rotate_transaction_log()
                
                self.logger.info(f"Checkpoint created: {checkpoint_path}")
                return checkpoint_path
            finally:
                # Clean up temporary directory
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            self.logger.error(f"Error creating checkpoint: {e}")
            return None
    
    def recover_from_checkpoint(self, checkpoint_path: str, 
                               target_dir: Optional[str] = None,
                               sources_to_recover: Optional[List[str]] = None) -> bool:
        """
        Recover from a checkpoint.
        
        Args:
            checkpoint_path: Path to the checkpoint file.
            target_dir: Optional directory to recover to. If None, original paths will be used.
            sources_to_recover: Optional list of source names to recover. If None, all sources will be recovered.
            
        Returns:
            True if recovery was successful, False otherwise.
        """
        try:
            if not os.path.exists(checkpoint_path):
                self.logger.error(f"Checkpoint file not found: {checkpoint_path}")
                return False
            
            # Create temporary directory for extraction
            temp_dir = os.path.join(self.recovery_dir, "temp_recovery")
            os.makedirs(temp_dir, exist_ok=True)
            
            try:
                # Extract checkpoint
                with zipfile.ZipFile(checkpoint_path, "r") as zipf:
                    zipf.extractall(temp_dir)
                
                # Load metadata
                metadata_path = os.path.join(temp_dir, "checkpoint_metadata.json")
                if not os.path.exists(metadata_path):
                    self.logger.error("Checkpoint metadata not found")
                    return False
                
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                
                # Recover each source
                for source_name, source_info in metadata["sources"].items():
                    # Skip if not in sources_to_recover
                    if sources_to_recover and source_name not in sources_to_recover:
                        continue
                    
                    source_type = source_info.get("type")
                    original_path = source_info.get("original_path")
                    checkpoint_path = source_info.get("checkpoint_path")
                    
                    # Determine target path
                    if target_dir and original_path:
                        # Use target directory with original filename
                        target_path = os.path.join(target_dir, os.path.basename(original_path))
                    elif target_dir:
                        # Use target directory with checkpoint filename
                        target_path = os.path.join(target_dir, checkpoint_path)
                    elif original_path:
                        # Use original path
                        target_path = original_path
                    else:
                        self.logger.warning(f"Cannot determine target path for {source_name}")
                        continue
                    
                    # Create target directory if it doesn't exist
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    
                    # Recover based on source type
                    if source_type == "file":
                        source_path = os.path.join(temp_dir, checkpoint_path)
                        shutil.copy2(source_path, target_path)
                        self.logger.info(f"Recovered file: {target_path}")
                    elif source_type == "sqlite":
                        source_path = os.path.join(temp_dir, checkpoint_path)
                        
                        # Close any existing connections
                        if os.path.exists(target_path):
                            try:
                                # Try to create a connection to check if database is locked
                                test_conn = sqlite3.connect(target_path)
                                test_conn.close()
                                
                                # If not locked, remove the existing database
                                os.remove(target_path)
                            except sqlite3.OperationalError:
                                self.logger.error(f"Cannot recover database {target_path}: database is locked")
                                continue
                        
                        # Copy the database file
                        shutil.copy2(source_path, target_path)
                        self.logger.info(f"Recovered database: {target_path}")
                    elif source_type == "json":
                        source_path = os.path.join(temp_dir, checkpoint_path)
                        shutil.copy2(source_path, target_path)
                        self.logger.info(f"Recovered JSON file: {target_path}")
                
                self.logger.info(f"Recovery completed from checkpoint: {checkpoint_path}")
                return True
            finally:
                # Clean up temporary directory
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            self.logger.error(f"Error recovering from checkpoint: {e}")
            return False
    
    def apply_transaction_log(self, target_dir: Optional[str] = None,
                             start_time: Optional[datetime.datetime] = None,
                             end_time: Optional[datetime.datetime] = None) -> bool:
        """
        Apply transactions from the transaction log.
        
        Args:
            target_dir: Optional directory to apply transactions to. If None, original paths will be used.
            start_time: Optional start time for transactions to apply.
            end_time: Optional end time for transactions to apply.
            
        Returns:
            True if application was successful, False otherwise.
        """
        try:
            if not os.path.exists(self.transaction_log_path):
                self.logger.warning("Transaction log not found")
                return False
            
            # Convert start and end times to strings for comparison
            start_time_str = start_time.isoformat() if start_time else None
            end_time_str = end_time.isoformat() if end_time else None
            
            # Read transaction log
            transactions = []
            with open(self.transaction_log_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        transaction = json.loads(line)
                        
                        # Filter by time range
                        timestamp = transaction.get("timestamp")
                        if start_time_str and timestamp < start_time_str:
                            continue
                        if end_time_str and timestamp > end_time_str:
                            continue
                        
                        transactions.append(transaction)
                    except json.JSONDecodeError:
                        self.logger.warning(f"Invalid transaction log entry: {line}")
            
            # Sort transactions by timestamp
            transactions.sort(key=lambda x: x.get("timestamp", ""))
            
            # Apply transactions
            applied_count = 0
            for transaction in transactions:
                if self._apply_transaction(transaction, target_dir):
                    applied_count += 1
            
            self.logger.info(f"Applied {applied_count} transactions from log")
            return True
        except Exception as e:
            self.logger.error(f"Error applying transaction log: {e}")
            return False
    
    def _apply_transaction(self, transaction: Dict[str, Any], 
                          target_dir: Optional[str] = None) -> bool:
        """
        Apply a single transaction.
        
        Args:
            transaction: Transaction to apply.
            target_dir: Optional directory to apply transaction to.
            
        Returns:
            True if application was successful, False otherwise.
        """
        try:
            transaction_type = transaction.get("transaction_type")
            entity_type = transaction.get("entity_type")
            entity_id = transaction.get("entity_id")
            operation = transaction.get("operation")
            data = transaction.get("data", {})
            
            # This is a simplified implementation
            # In a real system, you would have more sophisticated transaction application logic
            
            self.logger.info(f"Applied transaction: {transaction_type} {operation} on {entity_type} {entity_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error applying transaction: {e}")
            return False
    
    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """
        List available checkpoints.
        
        Returns:
            List of dictionaries containing checkpoint information.
        """
        try:
            checkpoints = []
            
            # Get all zip files in recovery directory
            for filename in os.listdir(self.recovery_dir):
                if filename.startswith("checkpoint_") and filename.endswith(".zip"):
                    file_path = os.path.join(self.recovery_dir, filename)
                    
                    # Get file stats
                    stats = os.stat(file_path)
                    
                    # Try to extract metadata
                    metadata = self._extract_checkpoint_metadata(file_path)
                    
                    checkpoints.append({
                        "filename": filename,
                        "path": file_path,
                        "size": stats.st_size,
                        "created_at": datetime.datetime.fromtimestamp(stats.st_ctime).isoformat(),
                        "metadata": metadata
                    })
            
            # Sort by creation time (newest first)
            checkpoints.sort(key=lambda x: x["created_at"], reverse=True)
            
            return checkpoints
        except Exception as e:
            self.logger.error(f"Error listing checkpoints: {e}")
            return []
    
    def _extract_checkpoint_metadata(self, checkpoint_path: str) -> Optional[Dict[str, Any]]:
        """
        Extract metadata from a checkpoint file.
        
        Args:
            checkpoint_path: Path to the checkpoint file.
            
        Returns:
            Dictionary containing checkpoint metadata, or None if extraction failed.
        """
        try:
            with zipfile.ZipFile(checkpoint_path, "r") as zipf:
                if "checkpoint_metadata.json" in zipf.namelist():
                    with zipf.open("checkpoint_metadata.json") as f:
                        return json.load(f)
            
            return None
        except Exception as e:
            self.logger.error(f"Error extracting checkpoint metadata: {e}")
            return None
    
    def _check_log_rotation(self) -> bool:
        """
        Check if log rotation is needed and rotate if necessary.
        
        Returns:
            True if rotation was performed, False otherwise.
        """
        try:
            # Check if transaction log exists
            if not os.path.exists(self.transaction_log_path):
                return False
            
            # Check log size
            log_size = os.path.getsize(self.transaction_log_path)
            
            if log_size >= self.max_log_size_bytes:
                return self._rotate_transaction_log()
            
            return False
        except Exception as e:
            self.logger.error(f"Error checking log rotation: {e}")
            return False
    
    def _rotate_transaction_log(self) -> bool:
        """
        Rotate the transaction log.
        
        Returns:
            True if rotation was successful, False otherwise.
        """
        try:
            # Check if transaction log exists
            if not os.path.exists(self.transaction_log_path):
                return False
            
            # Generate rotated log name
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            rotated_log_path = os.path.join(self.recovery_dir, f"transaction_{timestamp}.log")
            
            # Rename current log to rotated log
            shutil.move(self.transaction_log_path, rotated_log_path)
            
            # Create new empty log
            with open(self.transaction_log_path, "w") as f:
                pass
            
            self.logger.info(f"Rotated transaction log to: {rotated_log_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error rotating transaction log: {e}")
            return False
    
    def _load_checkpoint_info(self) -> Optional[datetime.datetime]:
        """
        Load checkpoint information.
        
        Returns:
            Datetime of last checkpoint, or None if not available.
        """
        try:
            if not os.path.exists(self.checkpoint_info_path):
                return None
            
            with open(self.checkpoint_info_path, "r") as f:
                info = json.load(f)
                
                if "last_checkpoint_time" in info:
                    return datetime.datetime.fromisoformat(info["last_checkpoint_time"])
                
                return None
        except Exception as e:
            self.logger.error(f"Error loading checkpoint info: {e}")
            return None
    
    def _save_checkpoint_info(self) -> bool:
        """
        Save checkpoint information.
        
        Returns:
            True if saving was successful, False otherwise.
        """
        try:
            info = {
                "last_checkpoint_time": self.last_checkpoint_time.isoformat() if self.last_checkpoint_time else None
            }
            
            with open(self.checkpoint_info_path, "w") as f:
                json.dump(info, f, indent=2)
            
            return True
        except Exception as e:
            self.logger.error(f"Error saving checkpoint info: {e}")
            return False
    
    def get_transaction_log_info(self) -> Dict[str, Any]:
        """
        Get information about the transaction log.
        
        Returns:
            Dictionary containing transaction log information.
        """
        try:
            info = {
                "exists": os.path.exists(self.transaction_log_path),
                "size": 0,
                "entry_count": 0,
                "first_entry_time": None,
                "last_entry_time": None
            }
            
            if info["exists"]:
                # Get file stats
                stats = os.stat(self.transaction_log_path)
                info["size"] = stats.st_size
                
                # Count entries and get timestamps
                with open(self.transaction_log_path, "r") as f:
                    first_entry = None
                    last_entry = None
                    entry_count = 0
                    
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        
                        try:
                            transaction = json.loads(line)
                            entry_count += 1
                            
                            if first_entry is None:
                                first_entry = transaction
                            
                            last_entry = transaction
                        except json.JSONDecodeError:
                            pass
                    
                    info["entry_count"] = entry_count
                    
                    if first_entry:
                        info["first_entry_time"] = first_entry.get("timestamp")
                    
                    if last_entry:
                        info["last_entry_time"] = last_entry.get("timestamp")
            
            return info
        except Exception as e:
            self.logger.error(f"Error getting transaction log info: {e}")
            return {
                "exists": False,
                "error": str(e)
            }