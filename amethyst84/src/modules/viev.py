"""
VIEV - Veritas Identity & Epistemic Validator
The Mirror Check

Monitors system integrity by tracking file changes, configuration shifts,
and structural modifications on the user's system. Detects when external
forces alter the environment without consent.

"The face in the mirror must match the face that looked."
"""

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict


@dataclass
class FileSignature:
    """Cryptographic identity of a single file."""
    path: str
    sha256: str
    size: int
    modified: float
    permissions: str
    snapshot_time: str


@dataclass
class IntegrityViolation:
    """A detected change to system structure."""
    timestamp: str
    violation_type: str  # MODIFIED, DELETED, CREATED, PERMISSION_CHANGED
    file_path: str
    details: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    old_signature: Optional[Dict] = None
    new_signature: Optional[Dict] = None


class VIEV:
    """
    Veritas Identity & Epistemic Validator

    Maintains a cryptographic baseline of critical system files and
    configurations. Detects unauthorized modifications, deletions,
    or additions that could indicate:

    - Corporate software pushing silent updates
    - AI platform config changes (Gemini, ChatGPT settings)
    - Browser extension modifications
    - Privacy setting rollbacks
    - Data collection enablement
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.baseline: Dict[str, FileSignature] = {}
        self.violations: List[IntegrityViolation] = []
        self.monitored_paths: Set[str] = set()
        self.baseline_path = self.config.get(
            "baseline_path", "config/viev_baseline.json"
        )
        self._setup_default_monitors()

    def _setup_default_monitors(self):
        """Set up default paths to monitor based on OS."""
        import platform
        system = platform.system()

        # Common browser and AI platform paths
        home = str(Path.home())

        if system == "Windows":
            self.monitored_paths.update([
                os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Preferences"),
                os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Secure Preferences"),
                os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data", "Local State"),
                os.path.join(home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Preferences"),
                os.path.join(home, "AppData", "Roaming", "Mozilla", "Firefox", "profiles.ini"),
                # Windows hosts file
                os.path.join(os.environ.get("SYSTEMROOT", "C:\\Windows"), "System32", "drivers", "etc", "hosts"),
                # Google Cloud SDK config
                os.path.join(home, "AppData", "Roaming", "gcloud", "properties"),
                os.path.join(home, "AppData", "Roaming", "gcloud", "credentials.db"),
            ])
        elif system == "Darwin":  # macOS
            self.monitored_paths.update([
                os.path.join(home, "Library", "Application Support", "Google", "Chrome", "Default", "Preferences"),
                os.path.join(home, "Library", "Application Support", "Google", "Chrome", "Local State"),
                os.path.join(home, "Library", "Preferences", "com.google.Chrome.plist"),
                os.path.join(home, "Library", "Application Support", "Firefox", "profiles.ini"),
                os.path.join(home, "Library", "Safari", "Bookmarks.plist"),
                "/etc/hosts",
                os.path.join(home, ".config", "gcloud", "properties"),
            ])
        else:  # Linux
            self.monitored_paths.update([
                os.path.join(home, ".config", "google-chrome", "Default", "Preferences"),
                os.path.join(home, ".config", "google-chrome", "Local State"),
                os.path.join(home, ".mozilla", "firefox", "profiles.ini"),
                "/etc/hosts",
                "/etc/resolv.conf",
                os.path.join(home, ".config", "gcloud", "properties"),
            ])

        # Common cross-platform paths
        self.monitored_paths.update([
            os.path.join(home, ".gitconfig"),
            os.path.join(home, ".ssh", "config"),
            os.path.join(home, ".npmrc"),
        ])

    def add_monitored_path(self, path: str):
        """Add a custom path to monitor."""
        self.monitored_paths.add(path)

    def add_monitored_directory(self, directory: str, extensions: Optional[List[str]] = None):
        """Add all files in a directory to monitoring."""
        if not os.path.isdir(directory):
            return
        for root, dirs, files in os.walk(directory):
            for f in files:
                if extensions:
                    if any(f.endswith(ext) for ext in extensions):
                        self.monitored_paths.add(os.path.join(root, f))
                else:
                    self.monitored_paths.add(os.path.join(root, f))

    def _hash_file(self, filepath: str) -> Optional[str]:
        """Generate SHA-256 hash of a file."""
        try:
            sha256 = hashlib.sha256()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except (IOError, PermissionError):
            return None

    def _get_file_signature(self, filepath: str) -> Optional[FileSignature]:
        """Get complete signature for a file."""
        try:
            if not os.path.exists(filepath):
                return None
            stat = os.stat(filepath)
            file_hash = self._hash_file(filepath)
            if file_hash is None:
                return None
            return FileSignature(
                path=filepath,
                sha256=file_hash,
                size=stat.st_size,
                modified=stat.st_mtime,
                permissions=oct(stat.st_mode),
                snapshot_time=datetime.now(timezone.utc).isoformat(),
            )
        except (OSError, PermissionError):
            return None

    def create_baseline(self) -> Dict[str, int]:
        """
        Create a cryptographic baseline of all monitored files.
        This is the 'identity snapshot' - the face in the mirror.

        Returns:
            Summary of files baselined
        """
        self.baseline.clear()
        stats = {"monitored": 0, "baselined": 0, "inaccessible": 0, "missing": 0}

        for path in self.monitored_paths:
            stats["monitored"] += 1
            if not os.path.exists(path):
                stats["missing"] += 1
                continue
            sig = self._get_file_signature(path)
            if sig:
                self.baseline[path] = sig
                stats["baselined"] += 1
            else:
                stats["inaccessible"] += 1

        self._save_baseline()
        return stats

    def _save_baseline(self):
        """Save baseline to disk."""
        os.makedirs(os.path.dirname(self.baseline_path), exist_ok=True)
        data = {
            path: asdict(sig) for path, sig in self.baseline.items()
        }
        with open(self.baseline_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_baseline(self) -> bool:
        """Load baseline from disk."""
        if not os.path.exists(self.baseline_path):
            return False
        try:
            with open(self.baseline_path, 'r') as f:
                data = json.load(f)
            self.baseline = {
                path: FileSignature(**sig_data)
                for path, sig_data in data.items()
            }
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    def scan(self) -> List[IntegrityViolation]:
        """
        Scan all monitored files against the baseline.
        This is the mirror check - does the face still match?

        Returns:
            List of detected violations
        """
        if not self.baseline:
            if not self.load_baseline():
                return []

        new_violations = []
        now = datetime.now(timezone.utc).isoformat()

        # Check existing baselined files
        for path, old_sig in self.baseline.items():
            if not os.path.exists(path):
                # File was deleted
                violation = IntegrityViolation(
                    timestamp=now,
                    violation_type="DELETED",
                    file_path=path,
                    details=f"File was deleted. Original hash: {old_sig.sha256[:16]}...",
                    severity="HIGH",
                    old_signature=asdict(old_sig),
                )
                new_violations.append(violation)
                continue

            new_sig = self._get_file_signature(path)
            if new_sig is None:
                violation = IntegrityViolation(
                    timestamp=now,
                    violation_type="INACCESSIBLE",
                    file_path=path,
                    details="File exists but cannot be read. Permissions may have changed.",
                    severity="HIGH",
                    old_signature=asdict(old_sig),
                )
                new_violations.append(violation)
                continue

            # Check hash
            if new_sig.sha256 != old_sig.sha256:
                violation = IntegrityViolation(
                    timestamp=now,
                    violation_type="MODIFIED",
                    file_path=path,
                    details=(
                        f"Content changed. "
                        f"Old hash: {old_sig.sha256[:16]}... "
                        f"New hash: {new_sig.sha256[:16]}... "
                        f"Size: {old_sig.size} -> {new_sig.size}"
                    ),
                    severity=self._classify_modification_severity(path),
                    old_signature=asdict(old_sig),
                    new_signature=asdict(new_sig),
                )
                new_violations.append(violation)

            # Check permissions
            elif new_sig.permissions != old_sig.permissions:
                violation = IntegrityViolation(
                    timestamp=now,
                    violation_type="PERMISSION_CHANGED",
                    file_path=path,
                    details=(
                        f"Permissions changed: {old_sig.permissions} -> {new_sig.permissions}"
                    ),
                    severity="MEDIUM",
                    old_signature=asdict(old_sig),
                    new_signature=asdict(new_sig),
                )
                new_violations.append(violation)

        # Check for new files in monitored directories
        for path in self.monitored_paths:
            if path not in self.baseline and os.path.exists(path):
                new_sig = self._get_file_signature(path)
                if new_sig:
                    violation = IntegrityViolation(
                        timestamp=now,
                        violation_type="CREATED",
                        file_path=path,
                        details=f"New file detected. Hash: {new_sig.sha256[:16]}...",
                        severity="MEDIUM",
                        new_signature=asdict(new_sig),
                    )
                    new_violations.append(violation)

        self.violations.extend(new_violations)
        return new_violations

    def _classify_modification_severity(self, filepath: str) -> str:
        """Classify how severe a file modification is."""
        critical_patterns = ["hosts", "credentials", "Secure Preferences", "Local State"]
        high_patterns = ["Preferences", "config", "properties", ".ssh"]
        medium_patterns = [".gitconfig", ".npmrc", "profiles.ini"]

        for pattern in critical_patterns:
            if pattern in filepath:
                return "CRITICAL"
        for pattern in high_patterns:
            if pattern in filepath:
                return "HIGH"
        for pattern in medium_patterns:
            if pattern in filepath:
                return "MEDIUM"
        return "LOW"

    def get_report(self) -> Dict:
        """Generate integrity report."""
        return {
            "module": "VIEV - Veritas Identity & Epistemic Validator",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "baseline_files": len(self.baseline),
            "monitored_paths": len(self.monitored_paths),
            "total_violations": len(self.violations),
            "violations_by_type": self._count_by_type(),
            "violations_by_severity": self._count_by_severity(),
            "violations": [asdict(v) for v in self.violations[-50:]],  # Last 50
        }

    def _count_by_type(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for v in self.violations:
            counts[v.violation_type] = counts.get(v.violation_type, 0) + 1
        return counts

    def _count_by_severity(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for v in self.violations:
            counts[v.severity] = counts.get(v.severity, 0) + 1
        return counts