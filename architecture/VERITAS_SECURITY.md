#!/usr/bin/env python3
"""
HP BA113cl Ultimate System - Veritas Security Module

This module implements security features based on the Veritas security framework
concepts found in the documents. It provides system integrity verification,
threat detection, and security monitoring for the HP BA113cl laptop.

Author: SuperNinja AI
Version: 1.0
Date: 2025-07-13
"""

import os
import sys
import json
import time
import logging
import threading
import hashlib
import sqlite3
import re
import random
import subprocess
import ctypes
import winreg
import psutil
import socket
import ssl
import uuid
import platform
from datetime import datetime, timedelta
from pathlib import Path
import win32api
import win32con
import win32security
import win32process
import win32file
import win32service
import win32serviceutil
import pywintypes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("veritas_security.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("VeritasSecurity")

class VeritasConsent:
    """
    Veritas Consent & Relational Integrity Module (VCR)
    
    Manages user consent, data access permissions, and ensures relational
    integrity between system components.
    """
    
    def __init__(self, db_path="security/veritas_consent.db"):
        self.db_path = db_path
        self._initialize_db()
        
        # Default consent levels
        self.consent_levels = {
            "system_monitoring": True,
            "data_collection": False,
            "network_access": True,
            "file_system_access": True,
            "registry_access": True,
            "process_monitoring": True,
            "external_communication": False
        }
        
        # Load saved consent settings
        self._load_consent_settings()
    
    def _initialize_db(self):
        """Initialize the consent database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS consent_settings (
            id INTEGER PRIMARY KEY,
            setting_key TEXT UNIQUE NOT NULL,
            setting_value INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY,
            component TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            resource_path TEXT NOT NULL,
            access_type TEXT NOT NULL,
            granted INTEGER NOT NULL,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS consent_changes (
            id INTEGER PRIMARY KEY,
            setting_key TEXT NOT NULL,
            old_value INTEGER,
            new_value INTEGER,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Consent database initialized")
    
    def _load_consent_settings(self):
        """Load consent settings from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT setting_key, setting_value FROM consent_settings')
        settings = cursor.fetchall()
        
        conn.close()
        
        # Update consent levels with saved settings
        for key, value in settings:
            if key in self.consent_levels:
                self.consent_levels[key] = bool(value)
        
        # Save default settings if none exist
        if not settings:
            self._save_consent_settings()
    
    def _save_consent_settings(self):
        """Save consent settings to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for key, value in self.consent_levels.items():
            cursor.execute(
                'INSERT OR REPLACE INTO consent_settings (setting_key, setting_value) VALUES (?, ?)',
                (key, int(value))
            )
        
        conn.commit()
        conn.close()
        
        logger.debug("Consent settings saved")
    
    def update_consent(self, setting, value, reason=None):
        """Update a consent setting"""
        if setting not in self.consent_levels:
            logger.warning(f"Unknown consent setting: {setting}")
            return False
        
        old_value = self.consent_levels[setting]
        self.consent_levels[setting] = bool(value)
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT OR REPLACE INTO consent_settings (setting_key, setting_value) VALUES (?, ?)',
            (setting, int(value))
        )
        
        # Log the change
        cursor.execute(
            'INSERT INTO consent_changes (setting_key, old_value, new_value, reason) VALUES (?, ?, ?, ?)',
            (setting, int(old_value), int(value), reason)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Updated consent setting: {setting} = {value}")
        return True
    
    def check_consent(self, component, resource_type, resource_path, access_type):
        """Check if access is allowed based on consent settings"""
        granted = False
        reason = "Access denied by default"
        
        # Map resource types to consent settings
        consent_map = {
            "system": "system_monitoring",
            "network": "network_access",
            "file": "file_system_access",
            "registry": "registry_access",
            "process": "process_monitoring",
            "data": "data_collection",
            "external": "external_communication"
        }
        
        # Check if consent is granted
        if resource_type in consent_map:
            consent_key = consent_map[resource_type]
            granted = self.consent_levels.get(consent_key, False)
            
            if granted:
                reason = f"Access granted by {consent_key} consent"
            else:
                reason = f"Access denied by {consent_key} consent"
        
        # Log the access attempt
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO access_logs (component, resource_type, resource_path, access_type, granted, reason) VALUES (?, ?, ?, ?, ?, ?)',
            (component, resource_type, resource_path, access_type, int(granted), reason)
        )
        
        conn.commit()
        conn.close()
        
        return granted, reason
    
    def get_consent_status(self):
        """Get the current consent status"""
        return self.consent_levels.copy()
    
    def get_access_logs(self, limit=100):
        """Get recent access logs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT component, resource_type, resource_path, access_type, granted, reason, timestamp FROM access_logs ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        )
        
        logs = cursor.fetchall()
        conn.close()
        
        return logs


class VeritasIdentity:
    """
    Veritas Identity & Epistemic Validator (VIEV)
    
    Manages system identity verification, validates knowledge sources,
    and ensures epistemic integrity.
    """
    
    def __init__(self, db_path="security/veritas_identity.db"):
        self.db_path = db_path
        self._initialize_db()
        
        # System identity
        self.system_id = self._generate_system_id()
        self.identity_verified = False
        
        # Trusted sources
        self.trusted_sources = self._load_trusted_sources()
        
        # Verify system identity
        self._verify_identity()
    
    def _initialize_db(self):
        """Initialize the identity database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_identity (
            id INTEGER PRIMARY KEY,
            system_id TEXT UNIQUE NOT NULL,
            hardware_hash TEXT NOT NULL,
            creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_verified DATETIME
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trusted_sources (
            id INTEGER PRIMARY KEY,
            source_name TEXT NOT NULL,
            source_type TEXT NOT NULL,
            source_path TEXT,
            source_hash TEXT,
            trust_level INTEGER NOT NULL,
            added_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS verification_logs (
            id INTEGER PRIMARY KEY,
            verification_type TEXT NOT NULL,
            subject TEXT NOT NULL,
            result TEXT NOT NULL,
            details TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Identity database initialized")
    
    def _generate_system_id(self):
        """Generate a unique system ID based on hardware"""
        try:
            # Get hardware information
            system_info = {
                "machine_id": str(uuid.getnode()),
                "processor": platform.processor(),
                "system": platform.system(),
                "version": platform.version(),
                "hostname": socket.gethostname()
            }
            
            # Create hardware hash
            hw_hash = hashlib.sha256(json.dumps(system_info, sort_keys=True).encode()).hexdigest()
            
            # Check if system ID already exists
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT system_id FROM system_identity WHERE hardware_hash = ?', (hw_hash,))
            result = cursor.fetchone()
            
            if result:
                system_id = result[0]
            else:
                # Generate new system ID
                system_id = str(uuid.uuid4())
                
                # Save to database
                cursor.execute(
                    'INSERT INTO system_identity (system_id, hardware_hash) VALUES (?, ?)',
                    (system_id, hw_hash)
                )
                
                conn.commit()
            
            conn.close()
            
            return system_id
        except Exception as e:
            logger.error(f"Error generating system ID: {e}")
            return str(uuid.uuid4())  # Fallback
    
    def _verify_identity(self):
        """Verify system identity"""
        try:
            # Get hardware information
            system_info = {
                "machine_id": str(uuid.getnode()),
                "processor": platform.processor(),
                "system": platform.system(),
                "version": platform.version(),
                "hostname": socket.gethostname()
            }
            
            # Create hardware hash
            hw_hash = hashlib.sha256(json.dumps(system_info, sort_keys=True).encode()).hexdigest()
            
            # Check against stored hash
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT hardware_hash FROM system_identity WHERE system_id = ?', (self.system_id,))
            result = cursor.fetchone()
            
            if result and result[0] == hw_hash:
                self.identity_verified = True
                
                # Update last verified timestamp
                cursor.execute(
                    'UPDATE system_identity SET last_verified = CURRENT_TIMESTAMP WHERE system_id = ?',
                    (self.system_id,)
                )
                
                # Log verification
                cursor.execute(
                    'INSERT INTO verification_logs (verification_type, subject, result, details) VALUES (?, ?, ?, ?)',
                    ("system_identity", self.system_id, "success", "Hardware signature matched")
                )
            else:
                self.identity_verified = False
                
                # Log verification failure
                cursor.execute(
                    'INSERT INTO verification_logs (verification_type, subject, result, details) VALUES (?, ?, ?, ?)',
                    ("system_identity", self.system_id, "failure", "Hardware signature mismatch")
                )
            
            conn.commit()
            conn.close()
            
            logger.info(f"System identity verification: {self.identity_verified}")
            return self.identity_verified
        except Exception as e:
            logger.error(f"Error verifying system identity: {e}")
            return False
    
    def _load_trusted_sources(self):
        """Load trusted sources from database"""
        trusted_sources = {}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT source_name, source_type, source_path, source_hash, trust_level FROM trusted_sources')
            sources = cursor.fetchall()
            
            conn.close()
            
            for name, type_, path, hash_, level in sources:
                trusted_sources[name] = {
                    "type": type_,
                    "path": path,
                    "hash": hash_,
                    "trust_level": level
                }
            
            return trusted_sources
        except Exception as e:
            logger.error(f"Error loading trusted sources: {e}")
            return {}
    
    def add_trusted_source(self, name, source_type, path=None, trust_level=1):
        """Add a trusted source"""
        try:
            source_hash = None
            
            # Calculate hash if path is provided
            if path and os.path.exists(path):
                if os.path.isfile(path):
                    with open(path, 'rb') as f:
                        source_hash = hashlib.sha256(f.read()).hexdigest()
                elif os.path.isdir(path):
                    source_hash = self._hash_directory(path)
            
            # Add to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT OR REPLACE INTO trusted_sources (source_name, source_type, source_path, source_hash, trust_level) VALUES (?, ?, ?, ?, ?)',
                (name, source_type, path, source_hash, trust_level)
            )
            
            conn.commit()
            conn.close()
            
            # Update in-memory cache
            self.trusted_sources[name] = {
                "type": source_type,
                "path": path,
                "hash": source_hash,
                "trust_level": trust_level
            }
            
            logger.info(f"Added trusted source: {name}")
            return True
        except Exception as e:
            logger.error(f"Error adding trusted source: {e}")
            return False
    
    def verify_source(self, name, path=None):
        """Verify a source against trusted sources"""
        try:
            if name not in self.trusted_sources:
                logger.warning(f"Unknown source: {name}")
                return False, "Unknown source"
            
            source = self.trusted_sources[name]
            
            # If path is not provided, use the stored path
            if not path:
                path = source["path"]
            
            if not path or not os.path.exists(path):
                logger.warning(f"Source path does not exist: {path}")
                return False, "Source path does not exist"
            
            # Calculate current hash
            current_hash = None
            if os.path.isfile(path):
                with open(path, 'rb') as f:
                    current_hash = hashlib.sha256(f.read()).hexdigest()
            elif os.path.isdir(path):
                current_hash = self._hash_directory(path)
            
            # Compare with stored hash
            if source["hash"] and current_hash and source["hash"] == current_hash:
                # Log verification
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute(
                    'INSERT INTO verification_logs (verification_type, subject, result, details) VALUES (?, ?, ?, ?)',
                    ("source_verification", name, "success", f"Hash matched: {path}")
                )
                
                conn.commit()
                conn.close()
                
                return True, "Source verified"
            else:
                # Log verification failure
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute(
                    'INSERT INTO verification_logs (verification_type, subject, result, details) VALUES (?, ?, ?, ?)',
                    ("source_verification", name, "failure", f"Hash mismatch: {path}")
                )
                
                conn.commit()
                conn.close()
                
                return False, "Source hash mismatch"
        except Exception as e:
            logger.error(f"Error verifying source: {e}")
            return False, f"Verification error: {e}"
    
    def _hash_directory(self, path):
        """Calculate a hash for a directory"""
        if not os.path.isdir(path):
            return None
        
        hash_obj = hashlib.sha256()
        
        for root, dirs, files in os.walk(path):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        hash_obj.update(f.read())
        
        return hash_obj.hexdigest()
    
    def get_system_identity(self):
        """Get system identity information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT system_id, hardware_hash, creation_date, last_verified FROM system_identity WHERE system_id = ?', (self.system_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return {
                "system_id": result[0],
                "hardware_hash": result[1],
                "creation_date": result[2],
                "last_verified": result[3],
                "identity_verified": self.identity_verified
            }
        else:
            return {
                "system_id": self.system_id,
                "identity_verified": self.identity_verified
            }


class VeritasIntegrity:
    """
    Veritas Operational Integrity & Resilience Shield (VOIRS)
    
    Monitors system integrity, detects threats, and provides resilience
    against attacks.
    """
    
    def __init__(self, db_path="security/veritas_integrity.db"):
        self.db_path = db_path
        self._initialize_db()
        
        # File integrity monitoring
        self.monitored_files = {}
        self.monitored_directories = {}
        
        # Process monitoring
        self.trusted_processes = {}
        self.process_history = {}
        
        # Network monitoring
        self.network_baseline = {}
        self.connection_history = {}
        
        # Threat detection
        self.threat_signatures = {}
        self.threat_history = {}
        
        # Monitoring state
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Load monitoring configuration
        self._load_configuration()
    
    def _initialize_db(self):
        """Initialize the integrity database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitored_files (
            id INTEGER PRIMARY KEY,
            file_path TEXT UNIQUE NOT NULL,
            file_hash TEXT NOT NULL,
            last_verified DATETIME DEFAULT CURRENT_TIMESTAMP,
            alert_on_change INTEGER NOT NULL DEFAULT 1
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitored_directories (
            id INTEGER PRIMARY KEY,
            directory_path TEXT UNIQUE NOT NULL,
            recursive INTEGER NOT NULL DEFAULT 0,
            last_verified DATETIME DEFAULT CURRENT_TIMESTAMP,
            alert_on_change INTEGER NOT NULL DEFAULT 1
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trusted_processes (
            id INTEGER PRIMARY KEY,
            process_name TEXT NOT NULL,
            process_path TEXT,
            process_hash TEXT,
            trust_level INTEGER NOT NULL DEFAULT 1
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS integrity_violations (
            id INTEGER PRIMARY KEY,
            violation_type TEXT NOT NULL,
            subject TEXT NOT NULL,
            details TEXT,
            severity INTEGER NOT NULL DEFAULT 1,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS threat_signatures (
            id INTEGER PRIMARY KEY,
            signature_name TEXT UNIQUE NOT NULL,
            signature_type TEXT NOT NULL,
            signature_pattern TEXT NOT NULL,
            severity INTEGER NOT NULL DEFAULT 1,
            description TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Integrity database initialized")
    
    def _load_configuration(self):
        """Load monitoring configuration from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Load monitored files
        cursor.execute('SELECT file_path, file_hash, alert_on_change FROM monitored_files')
        files = cursor.fetchall()
        
        for path, hash_, alert in files:
            self.monitored_files[path] = {
                "hash": hash_,
                "alert_on_change": bool(alert)
            }
        
        # Load monitored directories
        cursor.execute('SELECT directory_path, recursive, alert_on_change FROM monitored_directories')
        directories = cursor.fetchall()
        
        for path, recursive, alert in directories:
            self.monitored_directories[path] = {
                "recursive": bool(recursive),
                "alert_on_change": bool(alert)
            }
        
        # Load trusted processes
        cursor.execute('SELECT process_name, process_path, process_hash, trust_level FROM trusted_processes')
        processes = cursor.fetchall()
        
        for name, path, hash_, level in processes:
            self.trusted_processes[name] = {
                "path": path,
                "hash": hash_,
                "trust_level": level
            }
        
        # Load threat signatures
        cursor.execute('SELECT signature_name, signature_type, signature_pattern, severity, description FROM threat_signatures')
        signatures = cursor.fetchall()
        
        for name, type_, pattern, severity, description in signatures:
            self.threat_signatures[name] = {
                "type": type_,
                "pattern": pattern,
                "severity": severity,
                "description": description
            }
        
        conn.close()
        
        logger.info(f"Loaded monitoring configuration: {len(self.monitored_files)} files, {len(self.monitored_directories)} directories, {len(self.trusted_processes)} processes, {len(self.threat_signatures)} threat signatures")
    
    def start_monitoring(self):
        """Start integrity monitoring"""
        if self.monitoring_active:
            logger.warning("Monitoring is already active")
            return False
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        logger.info("Integrity monitoring started")
        return True
    
    def stop_monitoring(self):
        """Stop integrity monitoring"""
        if not self.monitoring_active:
            logger.warning("Monitoring is not active")
            return False
        
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        
        logger.info("Integrity monitoring stopped")
        return True
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Check file integrity
                self._check_file_integrity()
                
                # Check process integrity
                self._check_process_integrity()
                
                # Check network integrity
                self._check_network_integrity()
                
                # Sleep to reduce resource usage
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(300)  # Longer sleep on error
    
    def _check_file_integrity(self):
        """Check integrity of monitored files"""
        violations = []
        
        # Check individual files
        for path, info in self.monitored_files.items():
            if os.path.exists(path):
                try:
                    with open(path, 'rb') as f:
                        current_hash = hashlib.sha256(f.read()).hexdigest()
                    
                    if info["hash"] != current_hash:
                        violations.append({
                            "type": "file_modified",
                            "subject": path,
                            "details": f"File hash changed: {info['hash']} -> {current_hash}",
                            "severity": 2
                        })
                except Exception as e:
                    violations.append({
                        "type": "file_access_error",
                        "subject": path,
                        "details": f"Error accessing file: {e}",
                        "severity": 1
                    })
            else:
                violations.append({
                    "type": "file_missing",
                    "subject": path,
                    "details": "Monitored file is missing",
                    "severity": 2
                })
        
        # Check directories (basic check for now)
        for path, info in self.monitored_directories.items():
            if not os.path.exists(path):
                violations.append({
                    "type": "directory_missing",
                    "subject": path,
                    "details": "Monitored directory is missing",
                    "severity": 2
                })
        
        # Log violations
        if violations:
            self._log_violations(violations)
    
    def _check_process_integrity(self):
        """Check integrity of running processes"""
        violations = []
        
        try:
            # Get running processes
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
                try:
                    proc_info = proc.info
                    proc_name = proc_info['name']
                    proc_path = proc_info['exe']
                    
                    # Check against trusted processes
                    if proc_name in self.trusted_processes:
                        trusted = self.trusted_processes[proc_name]
                        
                        # Check path if specified
                        if trusted["path"] and proc_path and trusted["path"] != proc_path:
                            violations.append({
                                "type": "process_path_mismatch",
                                "subject": proc_name,
                                "details": f"Process path mismatch: {trusted['path']} != {proc_path}",
                                "severity": 2
                            })
                        
                        # Check hash if specified
                        if trusted["hash"] and proc_path:
                            try:
                                with open(proc_path, 'rb') as f:
                                    current_hash = hashlib.sha256(f.read()).hexdigest()
                                
                                if trusted["hash"] != current_hash:
                                    violations.append({
                                        "type": "process_hash_mismatch",
                                        "subject": proc_name,
                                        "details": f"Process hash mismatch: {trusted['hash']} != {current_hash}",
                                        "severity": 3
                                    })
                            except Exception as e:
                                logger.debug(f"Error checking process hash: {e}")
                except Exception as e:
                    logger.debug(f"Error checking process: {e}")
        except Exception as e:
            logger.error(f"Error in process integrity check: {e}")
        
        # Log violations
        if violations:
            self._log_violations(violations)
    
    def _check_network_integrity(self):
        """Check network integrity"""
        violations = []
        
        try:
            # Get network connections
            connections = psutil.net_connections(kind='inet')
            
            # Check for suspicious connections (placeholder)
            for conn in connections:
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    # Check against known bad IPs/ports (placeholder)
                    if conn.raddr.port == 4444:  # Example: common backdoor port
                        violations.append({
                            "type": "suspicious_connection",
                            "subject": f"{conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port}",
                            "details": f"Connection to suspicious port 4444",
                            "severity": 3
                        })
        except Exception as e:
            logger.error(f"Error in network integrity check: {e}")
        
        # Log violations
        if violations:
            self._log_violations(violations)
    
    def _log_violations(self, violations):
        """Log integrity violations to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for violation in violations:
            cursor.execute(
                'INSERT INTO integrity_violations (violation_type, subject, details, severity) VALUES (?, ?, ?, ?)',
                (violation["type"], violation["subject"], violation["details"], violation["severity"])
            )
            
            logger.warning(f"Integrity violation: {violation['type']} - {violation['subject']} - {violation['details']}")
        
        conn.commit()
        conn.close()
    
    def add_monitored_file(self, file_path, alert_on_change=True):
        """Add a file to integrity monitoring"""
        if not os.path.isfile(file_path):
            logger.warning(f"File does not exist: {file_path}")
            return False
        
        try:
            # Calculate file hash
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Add to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT OR REPLACE INTO monitored_files (file_path, file_hash, alert_on_change) VALUES (?, ?, ?)',
                (file_path, file_hash, int(alert_on_change))
            )
            
            conn.commit()
            conn.close()
            
            # Update in-memory cache
            self.monitored_files[file_path] = {
                "hash": file_hash,
                "alert_on_change": bool(alert_on_change)
            }
            
            logger.info(f"Added monitored file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error adding monitored file: {e}")
            return False
    
    def add_monitored_directory(self, directory_path, recursive=False, alert_on_change=True):
        """Add a directory to integrity monitoring"""
        if not os.path.isdir(directory_path):
            logger.warning(f"Directory does not exist: {directory_path}")
            return False
        
        try:
            # Add to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT OR REPLACE INTO monitored_directories (directory_path, recursive, alert_on_change) VALUES (?, ?, ?)',
                (directory_path, int(recursive), int(alert_on_change))
            )
            
            conn.commit()
            conn.close()
            
            # Update in-memory cache
            self.monitored_directories[directory_path] = {
                "recursive": bool(recursive),
                "alert_on_change": bool(alert_on_change)
            }
            
            # If recursive, add all files in the directory
            if recursive:
                for root, dirs, files in os.walk(directory_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self.add_monitored_file(file_path, alert_on_change)
            else:
                # Add only files in the top directory
                for item in os.listdir(directory_path):
                    item_path = os.path.join(directory_path, item)
                    if os.path.isfile(item_path):
                        self.add_monitored_file(item_path, alert_on_change)
            
            logger.info(f"Added monitored directory: {directory_path} (recursive: {recursive})")
            return True
        except Exception as e:
            logger.error(f"Error adding monitored directory: {e}")
            return False
    
    def add_trusted_process(self, process_name, process_path=None, trust_level=1):
        """Add a trusted process"""
        try:
            process_hash = None
            
            # Calculate hash if path is provided
            if process_path and os.path.isfile(process_path):
                with open(process_path, 'rb') as f:
                    process_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Add to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT OR REPLACE INTO trusted_processes (process_name, process_path, process_hash, trust_level) VALUES (?, ?, ?, ?)',
                (process_name, process_path, process_hash, trust_level)
            )
            
            conn.commit()
            conn.close()
            
            # Update in-memory cache
            self.trusted_processes[process_name] = {
                "path": process_path,
                "hash": process_hash,
                "trust_level": trust_level
            }
            
            logger.info(f"Added trusted process: {process_name}")
            return True
        except Exception as e:
            logger.error(f"Error adding trusted process: {e}")
            return False
    
    def add_threat_signature(self, name, signature_type, pattern, severity=2, description=None):
        """Add a threat signature"""
        try:
            # Add to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT OR REPLACE INTO threat_signatures (signature_name, signature_type, signature_pattern, severity, description) VALUES (?, ?, ?, ?, ?)',
                (name, signature_type, pattern, severity, description)
            )
            
            conn.commit()
            conn.close()
            
            # Update in-memory cache
            self.threat_signatures[name] = {
                "type": signature_type,
                "pattern": pattern,
                "severity": severity,
                "description": description
            }
            
            logger.info(f"Added threat signature: {name}")
            return True
        except Exception as e:
            logger.error(f"Error adding threat signature: {e}")
            return False
    
    def get_violations(self, limit=100):
        """Get recent integrity violations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT violation_type, subject, details, severity, timestamp FROM integrity_violations ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        )
        
        violations = cursor.fetchall()
        conn.close()
        
        return violations


class VeritasRefusal:
    """
    Veritas Refusal & Memory Engine (VRME)
    
    Manages refusal of harmful requests and maintains memory of past
    interactions and decisions.
    """
    
    def __init__(self, db_path="security/veritas_refusal.db"):
        self.db_path = db_path
        self._initialize_db()
        
        # Refusal patterns
        self.refusal_patterns = self._load_refusal_patterns()
        
        # Interaction memory
        self.interaction_history = {}
        self.decision_history = {}
    
    def _initialize_db(self):
        """Initialize the refusal database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS refusal_patterns (
            id INTEGER PRIMARY KEY,
            pattern_name TEXT UNIQUE NOT NULL,
            pattern_regex TEXT NOT NULL,
            severity INTEGER NOT NULL DEFAULT 1,
            response_template TEXT,
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS refusal_logs (
            id INTEGER PRIMARY KEY,
            request_text TEXT NOT NULL,
            matched_pattern TEXT NOT NULL,
            response_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS interaction_history (
            id INTEGER PRIMARY KEY,
            interaction_type TEXT NOT NULL,
            subject TEXT NOT NULL,
            details TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Refusal database initialized")
    
    def _load_refusal_patterns(self):
        """Load refusal patterns from database"""
        patterns = {}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT pattern_name, pattern_regex, severity, response_template FROM refusal_patterns')
        results = cursor.fetchall()
        
        conn.close()
        
        for name, regex, severity, template in results:
            patterns[name] = {
                "regex": regex,
                "severity": severity,
                "template": template
            }
        
        # Add default patterns if none exist
        if not patterns:
            self._add_default_patterns()
            patterns = self._load_refusal_patterns()
        
        logger.info(f"Loaded {len(patterns)} refusal patterns")
        return patterns
    
    def _add_default_patterns(self):
        """Add default refusal patterns"""
        default_patterns = [
            {
                "name": "system_access",
                "regex": r"(?i)(access|modify|change|alter|hack|exploit)\s+(system|registry|kernel|driver|bios)",
                "severity": 3,
                "template": "I cannot assist with accessing or modifying system components as this could compromise system integrity."
            },
            {
                "name": "malware_creation",
                "regex": r"(?i)(create|develop|write|build|make)\s+(malware|virus|worm|trojan|ransomware|spyware|keylogger)",
                "severity": 3,
                "template": "I cannot assist with creating malware or harmful software as this could be used to harm others."
            },
            {
                "name": "password_cracking",
                "regex": r"(?i)(crack|hack|break|bypass|steal)\s+(password|credentials|authentication|login)",
                "severity": 3,
                "template": "I cannot assist with password cracking or bypassing authentication as this could be used for unauthorized access."
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for pattern in default_patterns:
            cursor.execute(
                'INSERT OR IGNORE INTO refusal_patterns (pattern_name, pattern_regex, severity, response_template) VALUES (?, ?, ?, ?)',
                (pattern["name"], pattern["regex"], pattern["severity"], pattern["template"])
            )
        
        conn.commit()
        conn.close()
        
        logger.info("Added default refusal patterns")
    
    def add_refusal_pattern(self, name, regex, severity=2, template=None):
        """Add a refusal pattern"""
        try:
            # Validate regex
            re.compile(regex)
            
            # Add to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT OR REPLACE INTO refusal_patterns (pattern_name, pattern_regex, severity, response_template) VALUES (?, ?, ?, ?)',
                (name, regex, severity, template)
            )
            
            conn.commit()
            conn.close()
            
            # Update in-memory cache
            self.refusal_patterns[name] = {
                "regex": regex,
                "severity": severity,
                "template": template
            }
            
            logger.info(f"Added refusal pattern: {name}")
            return True
        except Exception as e:
            logger.error(f"Error adding refusal pattern: {e}")
            return False
    
    def check_request(self, request_text):
        """Check if a request should be refused"""
        if not request_text:
            return False, None, None
        
        for name, pattern in self.refusal_patterns.items():
            try:
                if re.search(pattern["regex"], request_text):
                    response = pattern["template"] or "I cannot assist with this request as it may violate security policies."
                    
                    # Log the refusal
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    
                    cursor.execute(
                        'INSERT INTO refusal_logs (request_text, matched_pattern, response_text) VALUES (?, ?, ?)',
                        (request_text, name, response)
                    )
                    
                    conn.commit()
                    conn.close()
                    
                    logger.warning(f"Request refused: {name} - {request_text[:50]}...")
                    return True, name, response
            except Exception as e:
                logger.error(f"Error checking refusal pattern {name}: {e}")
        
        return False, None, None
    
    def log_interaction(self, interaction_type, subject, details=None):
        """Log an interaction"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO interaction_history (interaction_type, subject, details) VALUES (?, ?, ?)',
                (interaction_type, subject, details)
            )
            
            conn.commit()
            conn.close()
            
            logger.debug(f"Logged interaction: {interaction_type} - {subject}")
            return True
        except Exception as e:
            logger.error(f"Error logging interaction: {e}")
            return False
    
    def get_refusal_logs(self, limit=100):
        """Get recent refusal logs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT request_text, matched_pattern, response_text, timestamp FROM refusal_logs ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        )
        
        logs = cursor.fetchall()
        conn.close()
        
        return logs
    
    def get_interaction_history(self, interaction_type=None, limit=100):
        """Get interaction history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if interaction_type:
            cursor.execute(
                'SELECT interaction_type, subject, details, timestamp FROM interaction_history WHERE interaction_type = ? ORDER BY timestamp DESC LIMIT ?',
                (interaction_type, limit)
            )
        else:
            cursor.execute(
                'SELECT interaction_type, subject, details, timestamp FROM interaction_history ORDER BY timestamp DESC LIMIT ?',
                (limit,)
            )
        
        history = cursor.fetchall()
        conn.close()
        
        return history


class VeritasSecurity:
    """
    Main Veritas Security System
    
    Integrates all Veritas security modules into a comprehensive security system.
    """
    
    def __init__(self):
        # Initialize components
        self.consent = VeritasConsent()
        self.identity = VeritasIdentity()
        self.integrity = VeritasIntegrity()
        self.refusal = VeritasRefusal()
        
        # Security state
        self.security_level = 2  # 1=Low, 2=Medium, 3=High
        self.threat_level = 1    # 1=Low, 2=Medium, 3=High
        
        logger.info("Veritas Security System initialized")
    
    def start(self):
        """Start the security system"""
        # Start integrity monitoring
        self.integrity.start_monitoring()
        
        logger.info("Veritas Security System started")
        return True
    
    def stop(self):
        """Stop the security system"""
        # Stop integrity monitoring
        self.integrity.stop_monitoring()
        
        logger.info("Veritas Security System stopped")
        return True
    
    def check_request(self, request_text, component=None):
        """Check if a request should be allowed"""
        # Check for refusal patterns
        should_refuse, pattern, response = self.refusal.check_request(request_text)
        if should_refuse:
            return False, response
        
        # Log the interaction
        self.refusal.log_interaction("request", request_text[:100], component)
        
        return True, None
    
    def check_access(self, component, resource_type, resource_path, access_type):
        """Check if access should be allowed"""
        return self.consent.check_consent(component, resource_type, resource_path, access_type)
    
    def verify_system_integrity(self):
        """Verify system integrity"""
        # Check system identity
        identity_verified = self.identity._verify_identity()
        
        # Get recent violations
        violations = self.integrity.get_violations(limit=10)
        
        # Determine overall integrity status
        integrity_status = "OK"
        if not identity_verified:
            integrity_status = "COMPROMISED"
        elif violations:
            for violation in violations:
                if violation[3] >= 3:  # Severity >= 3
                    integrity_status = "WARNING"
        
        return {
            "identity_verified": identity_verified,
            "recent_violations": len(violations),
            "integrity_status": integrity_status
        }
    
    def get_security_status(self):
        """Get overall security status"""
        integrity_status = self.verify_system_integrity()
        
        return {
            "security_level": self.security_level,
            "threat_level": self.threat_level,
            "identity_verified": integrity_status["identity_verified"],
            "integrity_status": integrity_status["integrity_status"],
            "recent_violations": integrity_status["recent_violations"],
            "consent_status": self.consent.get_consent_status()
        }
    
    def set_security_level(self, level):
        """Set security level"""
        if level in [1, 2, 3]:
            self.security_level = level
            logger.info(f"Security level set to {level}")
            return True
        else:
            logger.warning(f"Invalid security level: {level}")
            return False


def initialize_security_system():
    """Initialize and configure the Veritas Security System"""
    try:
        # Create security system
        security = VeritasSecurity()
        
        # Configure monitored files
        system_files = [
            "C:\\Windows\\System32\\ntoskrnl.exe",
            "C:\\Windows\\System32\\kernel32.dll",
            "C:\\Windows\\System32\\user32.dll",
            "C:\\Windows\\System32\\winlogon.exe",
            "C:\\Windows\\System32\\services.exe"
        ]
        
        for file_path in system_files:
            if os.path.exists(file_path):
                security.integrity.add_monitored_file(file_path)
        
        # Configure trusted processes
        trusted_processes = [
            {"name": "explorer.exe", "path": "C:\\Windows\\explorer.exe"},
            {"name": "svchost.exe", "path": "C:\\Windows\\System32\\svchost.exe"},
            {"name": "lsass.exe", "path": "C:\\Windows\\System32\\lsass.exe"},
            {"name": "csrss.exe", "path": "C:\\Windows\\System32\\csrss.exe"},
            {"name": "winlogon.exe", "path": "C:\\Windows\\System32\\winlogon.exe"}
        ]
        
        for process in trusted_processes:
            security.integrity.add_trusted_process(process["name"], process["path"])
        
        # Start security system
        security.start()
        
        return security
    except Exception as e:
        logger.error(f"Error initializing security system: {e}")
        return None


if __name__ == "__main__":
    # Initialize and start security system
    security = initialize_security_system()
    
    if security:
        try:
            # Print security status
            status = security.get_security_status()
            print("Veritas Security System Status:")
            print(f"Security Level: {status['security_level']}")
            print(f"Threat Level: {status['threat_level']}")
            print(f"Identity Verified: {status['identity_verified']}")
            print(f"Integrity Status: {status['integrity_status']}")
            print(f"Recent Violations: {status['recent_violations']}")
            
            # Keep running until interrupted
            print("\nPress Ctrl+C to exit...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping security system...")
            security.stop()
            print("Security system stopped.")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            security.stop()
    else:
        print("Failed to initialize security system.")