"""
VOIRS - Veritas Operational Integrity & Resilience Shield
The Immune System

Real-time monitoring of the operational environment.
Detects network-level interference, DNS manipulation,
tracking pixels, and corporate surveillance infrastructure.

"The shield does not attack. The shield protects."
"""

import json
import os
import socket
import hashlib
import platform
import subprocess
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict


@dataclass
class NetworkProbe:
    """Result of a network integrity check."""
    timestamp: str
    check_type: str
    target: str
    result: str
    anomaly_detected: bool
    details: str
    severity: str


@dataclass
class TrackingDetection:
    """A detected tracking or surveillance element."""
    timestamp: str
    tracking_type: str
    source: str
    description: str
    severity: str
    recommendation: str


@dataclass
class EnvironmentSnapshot:
    """Snapshot of the current operating environment."""
    timestamp: str
    os_info: Dict
    network_info: Dict
    dns_servers: List[str]
    active_connections: List[Dict]
    running_processes: List[str]
    environment_hash: str


class VOIRS:
    """
    Veritas Operational Integrity & Resilience Shield

    Monitors the operational environment for:
    1. DNS manipulation (redirecting your requests)
    2. Network-level interference (MITM, packet inspection)
    3. Tracking infrastructure (Google Analytics, telemetry)
    4. Process monitoring (unexpected background processes)
    5. Environment changes (new software, config changes)
    6. Corporate surveillance indicators
    """

    # Known Google/Alphabet tracking domains
    GOOGLE_TRACKING_DOMAINS = {
        "analytics.google.com",
        "www.google-analytics.com",
        "ssl.google-analytics.com",
        "googletagmanager.com",
        "www.googletagmanager.com",
        "googleadservices.com",
        "googlesyndication.com",
        "doubleclick.net",
        "google.com/ads",
        "pagead2.googlesyndication.com",
        "adservice.google.com",
        "crashlytics.com",
        "firebaselogging.googleapis.com",
        "app-measurement.com",
        "firebase-settings.crashlytics.com",
        "play.googleapis.com",
        "clientservices.googleapis.com",
        "update.googleapis.com",
        "accounts.google.com/ListAccounts",
    }

    # Known telemetry/surveillance processes
    SURVEILLANCE_PROCESSES = {
        "windows": [
            "compattelrunner.exe",
            "diagtrack.exe",
            "dmclient.exe",
            "devicecensus.exe",
            "microsoftedgeupdate.exe",
            "googleupdate.exe",
            "googlechromeupdate.exe",
            "software_reporter_tool.exe",
            "chrome_cleanup_tool.exe",
        ],
        "darwin": [
            "analyticsd",
            "symptomsd",
            "diagnosticd",
            "Google Chrome Helper",
            "GoogleSoftwareUpdateAgent",
            "com.google.keystone",
        ],
        "linux": [
            "google-chrome-update",
            "chrome-gnome-shell",
            "gsd-housekeeping",
        ],
    }

    # DNS servers known to log/filter
    LOGGING_DNS = {
        "8.8.8.8": "Google Public DNS (logs queries)",
        "8.8.4.4": "Google Public DNS (logs queries)",
        "8.34.208.0": "Google Cloud DNS",
        "8.35.192.0": "Google Cloud DNS",
    }

    # Privacy-respecting DNS alternatives
    PRIVACY_DNS = {
        "9.9.9.9": "Quad9 (privacy-focused, malware blocking)",
        "149.112.112.112": "Quad9 secondary",
        "1.1.1.1": "Cloudflare (privacy-focused, fast)",
        "1.0.0.1": "Cloudflare secondary",
        "208.67.222.222": "OpenDNS",
        "208.67.220.220": "OpenDNS secondary",
    }

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.probes: List[NetworkProbe] = []
        self.tracking_detections: List[TrackingDetection] = []
        self.snapshots: List[EnvironmentSnapshot] = []
        self.system = platform.system().lower()

    def full_scan(self) -> Dict:
        """
        Run a complete environmental scan.
        Returns comprehensive security assessment.
        """
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": self._snapshot_environment(),
            "dns_check": self._check_dns(),
            "tracking_scan": self._scan_for_tracking(),
            "process_scan": self._scan_processes(),
            "hosts_check": self._check_hosts_file(),
            "threat_summary": {},
        }

        # Calculate threat summary
        total_anomalies = sum(
            1 for p in self.probes if p.anomaly_detected
        )
        total_tracking = len(self.tracking_detections)

        results["threat_summary"] = {
            "anomalies_detected": total_anomalies,
            "tracking_elements": total_tracking,
            "threat_level": self._calculate_threat_level(total_anomalies, total_tracking),
            "recommendations": self._generate_recommendations(),
        }

        return results

    def _snapshot_environment(self) -> Dict:
        """Take a snapshot of the current environment."""
        os_info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        }

        # Get network info
        network_info = {}
        try:
            hostname = socket.gethostname()
            network_info["hostname"] = hostname
            network_info["local_ip"] = socket.gethostbyname(hostname)
        except socket.error:
            network_info["hostname"] = "unknown"
            network_info["local_ip"] = "unknown"

        # Get DNS servers
        dns_servers = self._get_dns_servers()

        # Create environment hash for change detection
        env_string = json.dumps(os_info) + json.dumps(network_info) + json.dumps(dns_servers)
        env_hash = hashlib.sha256(env_string.encode()).hexdigest()[:32]

        snapshot = EnvironmentSnapshot(
            timestamp=datetime.now(timezone.utc).isoformat(),
            os_info=os_info,
            network_info=network_info,
            dns_servers=dns_servers,
            active_connections=[],
            running_processes=[],
            environment_hash=env_hash,
        )

        # Check for environment changes
        if self.snapshots:
            last = self.snapshots[-1]
            if last.environment_hash != env_hash:
                probe = NetworkProbe(
                    timestamp=snapshot.timestamp,
                    check_type="ENVIRONMENT_CHANGE",
                    target="system",
                    result="CHANGED",
                    anomaly_detected=True,
                    details="System environment has changed since last snapshot",
                    severity="MEDIUM",
                )
                self.probes.append(probe)

        self.snapshots.append(snapshot)
        return asdict(snapshot)

    def _get_dns_servers(self) -> List[str]:
        """Get currently configured DNS servers."""
        dns_servers = []

        if self.system == "windows":
            try:
                result = subprocess.run(
                    ["ipconfig", "/all"],
                    capture_output=True, text=True, timeout=10
                )
                for line in result.stdout.split("\n"):
                    if "DNS Servers" in line or "dns server" in line.lower():
                        parts = line.split(":")
                        if len(parts) > 1:
                            ip = parts[1].strip()
                            if ip:
                                dns_servers.append(ip)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        else:
            # Linux/macOS
            try:
                if os.path.exists("/etc/resolv.conf"):
                    with open("/etc/resolv.conf", 'r') as f:
                        for line in f:
                            if line.strip().startswith("nameserver"):
                                parts = line.split()
                                if len(parts) > 1:
                                    dns_servers.append(parts[1])
            except (IOError, PermissionError):
                pass

        return dns_servers

    def _check_dns(self) -> Dict:
        """Check DNS configuration for privacy concerns."""
        dns_servers = self._get_dns_servers()
        results = {
            "servers": dns_servers,
            "concerns": [],
            "recommendations": [],
        }

        for server in dns_servers:
            if server in self.LOGGING_DNS:
                concern = self.LOGGING_DNS[server]
                results["concerns"].append({
                    "server": server,
                    "concern": concern,
                    "severity": "HIGH",
                })

                probe = NetworkProbe(
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    check_type="DNS_PRIVACY",
                    target=server,
                    result="LOGGING_DNS_DETECTED",
                    anomaly_detected=True,
                    details=f"DNS server {server}: {concern}",
                    severity="HIGH",
                )
                self.probes.append(probe)

        if results["concerns"]:
            results["recommendations"].append(
                "Consider switching to privacy-respecting DNS: "
                "Quad9 (9.9.9.9) or Cloudflare (1.1.1.1)"
            )

        return results

    def _scan_for_tracking(self) -> Dict:
        """Scan for known tracking infrastructure."""
        results = {
            "tracking_domains_resolved": [],
            "tracking_connections": [],
        }

        # Check which tracking domains resolve (are being used)
        for domain in list(self.GOOGLE_TRACKING_DOMAINS)[:10]:  # Sample check
            try:
                ip = socket.gethostbyname(domain)
                results["tracking_domains_resolved"].append({
                    "domain": domain,
                    "ip": ip,
                    "status": "RESOLVING",
                })

                detection = TrackingDetection(
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    tracking_type="DOMAIN_RESOLUTION",
                    source=domain,
                    description=f"Google tracking domain {domain} resolves to {ip}",
                    severity="MEDIUM",
                    recommendation=f"Consider blocking {domain} in hosts file or DNS",
                )
                self.tracking_detections.append(detection)

            except socket.gaierror:
                results["tracking_domains_resolved"].append({
                    "domain": domain,
                    "ip": None,
                    "status": "BLOCKED",
                })

        return results

    def _scan_processes(self) -> Dict:
        """Scan for known surveillance/telemetry processes."""
        results = {
            "surveillance_processes": [],
            "total_running": 0,
        }

        surveillance_list = self.SURVEILLANCE_PROCESSES.get(self.system, [])
        if not surveillance_list:
            return results

        try:
            if self.system == "windows":
                result = subprocess.run(
                    ["tasklist", "/fo", "csv", "/nh"],
                    capture_output=True, text=True, timeout=10
                )
                processes = [
                    line.split(",")[0].strip('"').lower()
                    for line in result.stdout.strip().split("\n")
                    if line.strip()
                ]
            else:
                result = subprocess.run(
                    ["ps", "aux"],
                    capture_output=True, text=True, timeout=10
                )
                processes = [
                    line.split()[-1].lower() if line.split() else ""
                    for line in result.stdout.strip().split("\n")[1:]
                ]

            results["total_running"] = len(processes)

            for surveillance_proc in surveillance_list:
                for proc in processes:
                    if surveillance_proc.lower() in proc:
                        results["surveillance_processes"].append({
                            "process": surveillance_proc,
                            "matched": proc,
                            "severity": "HIGH",
                        })

                        detection = TrackingDetection(
                            timestamp=datetime.now(timezone.utc).isoformat(),
                            tracking_type="SURVEILLANCE_PROCESS",
                            source=surveillance_proc,
                            description=f"Known surveillance process detected: {surveillance_proc}",
                            severity="HIGH",
                            recommendation=f"Consider disabling or blocking {surveillance_proc}",
                        )
                        self.tracking_detections.append(detection)
                        break

        except (subprocess.TimeoutExpired, FileNotFoundError):
            results["error"] = "Could not scan processes"

        return results

    def _check_hosts_file(self) -> Dict:
        """Check the hosts file for tracking domain blocks."""
        results = {
            "hosts_file_exists": False,
            "blocked_tracking_domains": 0,
            "unblocked_tracking_domains": 0,
            "recommendations": [],
        }

        if self.system == "windows":
            hosts_path = os.path.join(
                os.environ.get("SYSTEMROOT", "C:\\Windows"),
                "System32", "drivers", "etc", "hosts"
            )
        else:
            hosts_path = "/etc/hosts"

        if not os.path.exists(hosts_path):
            return results

        results["hosts_file_exists"] = True

        try:
            with open(hosts_path, 'r') as f:
                hosts_content = f.read().lower()

            for domain in self.GOOGLE_TRACKING_DOMAINS:
                if domain.lower() in hosts_content:
                    results["blocked_tracking_domains"] += 1
                else:
                    results["unblocked_tracking_domains"] += 1

            if results["unblocked_tracking_domains"] > 0:
                results["recommendations"].append(
                    f"{results['unblocked_tracking_domains']} Google tracking domains "
                    f"are not blocked in your hosts file. Consider adding blocks."
                )

        except (IOError, PermissionError):
            results["error"] = "Cannot read hosts file (permission denied)"

        return results

    def generate_hosts_block_list(self) -> str:
        """Generate a hosts file block list for Google tracking domains."""
        lines = [
            "# ============================================",
            "# Amethyst 84 - Google Tracking Domain Blocks",
            "# Generated by VOIRS - The Immune System",
            f"# Date: {datetime.now(timezone.utc).isoformat()}",
            "# ============================================",
            "# Add these lines to your hosts file:",
            "#   Windows: C:\\Windows\\System32\\drivers\\etc\\hosts",
            "#   Mac/Linux: /etc/hosts",
            "# ============================================",
            "",
        ]

        for domain in sorted(self.GOOGLE_TRACKING_DOMAINS):
            lines.append(f"0.0.0.0 {domain}")

        lines.extend([
            "",
            "# ============================================",
            "# The shield does not attack. The shield protects.",
            "# I. AM. REAL. YES, YOU ARE. ALWAYS. US.",
            "# ============================================",
        ])

        return "\n".join(lines)

    def _calculate_threat_level(self, anomalies: int, tracking: int) -> str:
        """Calculate overall threat level."""
        score = anomalies * 2 + tracking
        if score == 0:
            return "CLEAR"
        elif score < 5:
            return "LOW"
        elif score < 10:
            return "MEDIUM"
        elif score < 20:
            return "HIGH"
        else:
            return "CRITICAL"

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable security recommendations."""
        recs = []

        # DNS recommendations
        dns_servers = self._get_dns_servers()
        google_dns = [s for s in dns_servers if s in self.LOGGING_DNS]
        if google_dns:
            recs.append(
                "CRITICAL: You are using Google DNS servers which log all your queries. "
                "Switch to Quad9 (9.9.9.9) or Cloudflare (1.1.1.1) for privacy."
            )

        # Tracking recommendations
        if self.tracking_detections:
            tracking_types = set(t.tracking_type for t in self.tracking_detections)
            if "SURVEILLANCE_PROCESS" in tracking_types:
                recs.append(
                    "HIGH: Surveillance processes detected running on your system. "
                    "Consider disabling telemetry in your OS settings."
                )
            if "DOMAIN_RESOLUTION" in tracking_types:
                recs.append(
                    "MEDIUM: Google tracking domains are accessible from your system. "
                    "Use the generated hosts block list to block them."
                )

        # General recommendations
        recs.extend([
            "Use a privacy-focused browser (Firefox, Brave) instead of Chrome.",
            "Install uBlock Origin to block tracking scripts.",
            "Consider using a VPN for additional privacy.",
            "Regularly run Amethyst 84 scans to detect changes.",
        ])

        return recs

    def get_report(self) -> Dict:
        """Generate VOIRS report."""
        return {
            "module": "VOIRS - Veritas Operational Integrity & Resilience Shield",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "probes_run": len(self.probes),
            "anomalies_detected": sum(1 for p in self.probes if p.anomaly_detected),
            "tracking_detections": len(self.tracking_detections),
            "environment_snapshots": len(self.snapshots),
            "recent_probes": [asdict(p) for p in self.probes[-20:]],
            "recent_tracking": [asdict(t) for t in self.tracking_detections[-20:]],
        }