# this is the killswitch



#!/bin/bash

# GOOGLE KILLSWITCH IMPLEMENTATION SCRIPT
# Version: 1.0
# Platform: Kali Linux
# Security Level: Maximum

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KILLSWITCH_DIR="/usr/local/etc/google-killswitch"
LOG_FILE="/var/log/google-killswitch.log"
SERVICE_FILE="/etc/systemd/system/google-killswitch.service"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}This script must be run as root${NC}" >&2
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    log "Installing dependencies..."
    apt update
    apt install -y iptables systemd tcpdump conntrack dnsutils openssl net-tools
    log "Dependencies installed successfully"
}

# Create killswitch directory structure
create_directories() {
    log "Creating directory structure..."
    mkdir -p "$KILLSWITCH_DIR"/{bin,config,logs}
    mkdir -p /var/local/share/google-killswitch
    log "Directories created"
}

# Create Google domain blocklist
create_blocklist() {
    log "Creating Google domain blocklist..."
    cat > "$KILLSWITCH_DIR/config/google-domains.txt" << 'EOF'
google.com
*.google.com
googleapis.com
*.googleapis.com
googleusercontent.com
*.googleusercontent.com
google-analytics.com
*.google-analytics.com
googlesyndication.com
*.googlesyndication.com
googleadservices.com
*.googleadservices.com
googletraveladservices.com
*.googletraveladservices.com
doubleclick.net
*.doubleclick.net
googletagmanager.com
*.googletagmanager.com
googleoptimize.com
*.googleoptimize.com
googlevideo.com
*.googlevideo.com
googleusercontent.com
*.googleusercontent.com
google.co.in
*.google.co.in
google.co.uk
*.google.co.uk
google.de
*.google.de
google.fr
*.google.fr
google.jp
*.google.jp
google.cn
*.google.cn
google.ru
*.google.ru
google.ca
*.google.ca
google.au
*.google.au
google.es
*.google.es
google.it
*.google.it
google.nl
*.google.nl
google.se
*.google.se
google.no
*.google.no
google.dk
*.google.dk
google.fi
*.google.fi
google.ch
*.google.ch
google.at
*.google.at
google.be
*.google.be
google.ie
*.google.ie
google.pt
*.google.pt
google.gr
*.google.gr
google.pl
*.google.pl
google.cz
*.google.cz
google.hu
*.google.hu
google.ro
*.google.ro
google.bg
*.google.bg
google.hr
*.google.hr
google.si
*.google.si
google.sk
*.google.sk
google.ee
*.google.ee
google.lv
*.google.lv
google.lt
*.google.lt
google.ua
*.google.ua
google.by
*.google.by
google.rs
*.google.rs
google.me
*.google.me
google.ba
*.google.ba
google.mk
*.google.mk
google.al
*.google.al
google.tr
*.google.tr
google.il
*.google.il
google.ae
*.google.ae
google.sa
*.google.sa
google.com.eg
*.google.com.eg
google.com.mx
*.google.com.mx
google.com.ar
*.google.com.ar
google.com.br
*.google.com.br
google.com.co
*.google.com.co
google.com.pe
*.google.com.pe
google.com.ve
*.google.com.ve
google.com.cl
*.google.com.cl
google.com.ec
*.google.com.ec
google.com.py
*.google.com.py
google.com.uy
*.google.com.uy
google.com.bo
*.google.com.bo
google.com.sv
*.google.com.sv
google.com.gt
*.google.com.gt
google.com.cu
*.google.com.cu
google.com.do
*.google.com.do
google.com.hn
*.google.com.hn
google.com.ni
*.google.com.ni
google.com.pa
*.google.com.pa
google.com.cr
*.google.com.cr
google.com.pr
*.google.com.pr
google.com.vn
*.google.com.vn
google.com.th
*.google.com.th
google.com.my
*.google.com.my
google.com.sg
*.google.com.sg
google.com.ph
*.google.com.ph
google.com.id
*.google.com.id
google.com.hk
*.google.com.hk
google.com.tw
*.google.com.tw
google.co.nz
*.google.co.nz
google.co.za
*.google.co.za
google.co.ao
*.google.co.ao
google.co.bw
*.google.co.bw
google.co.ke
*.google.co.ke
google.co.ug
*.google.co.ug
google.co.tz
*.google.co.tz
google.co.zm
*.google.co.zm
google.co.zw
*.google.co.zw
google.co.mw
*.google.co.mw
google.co.sz
*.google.co.sz
google.co.ls
*.google.co.ls
google.co.na
*.google.co.na
google.co.bj
*.google.co.bj
google.co.ci
*.google.co.ci
google.co.cm
*.google.co.cm
google.co.ga
*.google.co.ga
google.co.tg
*.google.co.tg
google.co.cf
*.google.co.cf
google.co.cd
*.google.co.cd
google.co.ao
*.google.co.ao
google.co.gq
*.google.co.gq
google.co.st
*.google.co.st
google.co.sc
*.google.co.sc
google.co.mu
*.google.co.mu
google.co.mg
*.google.co.mg
google.co.re
*.google.co.re
google.co.yt
*.google.co.yt
google.co.mz
*.google.co.mz
EOF
    log "Google domain blocklist created"
}

# Create IP blocklist
create_ip_blocklist() {
    log "Creating Google IP blocklist..."
    cat > "$KILLSWITCH_DIR/config/google-ips.txt" << 'EOF'
# Google IP ranges (AS15169, AS36040, AS43515)
8.8.8.0/24
8.8.4.0/24
74.125.0.0/16
173.194.0.0/16
209.85.128.0/17
216.58.192.0/19
216.239.32.0/19
64.233.160.0/19
66.102.0.0/20
72.14.192.0/18
108.177.8.0/21
142.250.0.0/15
172.217.0.0/16
172.253.0.0/16
173.255.112.0/20
208.65.152.0/22
208.67.216.0/21
208.67.224.0/20
23.236.48.0/20
23.251.0.0/16
34.0.0.0/15
34.64.0.0/10
34.128.0.0/10
35.184.0.0/13
35.192.0.0/14
35.196.0.0/15
35.200.0.0/13
35.208.0.0/12
35.224.0.0/12
35.240.0.0/13
104.154.0.0/15
104.196.0.0/14
104.200.0.0/13
104.208.0.0/12
104.224.0.0/11
107.167.160.0/19
107.178.192.0/18
108.59.80.0/20
108.170.192.0/18
108.177.0.0/17
130.211.0.0/16
142.250.0.0/15
146.148.0.0/16
162.216.148.0/22
162.222.176.0/21
172.217.0.0/16
172.253.0.0/16
173.194.0.0/16
173.255.112.0/20
192.158.28.0/22
199.192.112.0/22
199.223.232.0/21
207.223.160.0/20
208.65.152.0/22
208.67.216.0/21
208.67.224.0/20
209.85.128.0/17
216.58.192.0/19
216.239.32.0/19
EOF
    log "Google IP blocklist created"
}

# Create password setup script
create_password_setup() {
    log "Creating password setup script..."
    cat > "$KILLSWITCH_DIR/bin/setup-password.sh" << 'EOF'
#!/bin/bash

# Google Killswitch Password Setup
# This script sets up the password for the killswitch toggle

KILLSWITCH_DIR="/usr/local/etc/google-killswitch"
PASSWORD_FILE="$KILLSWITCH_DIR/config/password.hash"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Google Killswitch Password Setup${NC}"
echo "=================================="

# Check if password already exists
if [[ -f "$PASSWORD_FILE" ]]; then
    echo -e "${YELLOW}Warning: Password already exists. This will overwrite it.${NC}"
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
fi

# Get new password
while true; do
    read -s -p "Enter new password: " password
    echo
    read -s -p "Confirm password: " password_confirm
    echo
    
    if [[ "$password" == "$password_confirm" ]]; then
        if [[ ${#password} -ge 8 ]]; then
            break
        else
            echo -e "${RED}Password must be at least 8 characters long${NC}"
        fi
    else
        echo -e "${RED}Passwords do not match${NC}"
    fi
done

# Generate hash
password_hash=$(openssl passwd -6 "$password")

# Save hash
echo "$password_hash" > "$PASSWORD_FILE"
chmod 600 "$PASSWORD_FILE"

echo -e "${GREEN}Password set successfully!${NC}"
echo "You can now use: google-killswitch-toggle"
EOF

    chmod +x "$KILLSWITCH_DIR/bin/setup-password.sh"
    log "Password setup script created"
}

# Create toggle script
create_toggle_script() {
    log "Creating toggle script..."
    cat > "$KILLSWITCH_DIR/bin/toggle.sh" << 'EOF'
#!/bin/bash

# Google Killswitch Toggle Script
# Password-protected toggle for Google traffic blocking

KILLSWITCH_DIR="/usr/local/etc/google-killswitch"
PASSWORD_FILE="$KILLSWITCH_DIR/config/password.hash"
SERVICE_NAME="google-killswitch"
LOG_FILE="/var/log/google-killswitch.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Authentication function
authenticate() {
    local attempts=3
    local prompt="Enter Google Killswitch password: "
    
    if [[ ! -f "$PASSWORD_FILE" ]]; then
        echo -e "${RED}Password not set. Run 'sudo setup-password' first.${NC}"
        return 1
    fi
    
    local stored_hash=$(cat "$PASSWORD_FILE")
    
    for ((i=1; i<=attempts; i++)); do
        read -s -p "$prompt" input
        echo
        
        local input_hash=$(openssl passwd -6 "$input")
        if [[ "$input_hash" == "$stored_hash" ]]; then
            return 0
        fi
        
        if [[ $i -lt $attempts ]]; then
            echo -e "${RED}Authentication failed. Attempt $i of $attempts${NC}"
        else
            echo -e "${RED}Authentication failed. Access denied.${NC}"
            log "Failed authentication attempt from user $USER"
            return 1
        fi
    done
}

# Toggle functionality
toggle_killswitch() {
    if authenticate; then
        if systemctl is-active --quiet "$SERVICE_NAME"; then
            # Deactivate
            systemctl stop "$SERVICE_NAME"
            echo -e "${YELLOW}Google traffic UNBLOCKED - Use with caution${NC}"
            log "Killswitch DEACTIVATED by user $USER"
        else
            # Activate
            systemctl start "$SERVICE_NAME"
            echo -e "${GREEN}Google traffic BLOCKED - Protection active${NC}"
            log "Killswitch ACTIVATED by user $USER"
        fi
    else
        exit 1
    fi
}

# Status check
if [[ "${1:-}" == "status" ]]; then
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        echo -e "${GREEN}Google Killswitch: ACTIVE${NC}"
    else
        echo -e "${RED}Google Killswitch: INACTIVE${NC}"
    fi
    exit 0
fi

# Toggle
toggle_killswitch
EOF

    chmod +x "$KILLSWITCH_DIR/bin/toggle.sh"
    log "Toggle script created"
}

# Create activation script
create_activation_script() {
    log "Creating activation script..."
    cat > "$KILLSWITCH_DIR/bin/activate.sh" << 'EOF'
#!/bin/bash

# Google Killswitch Activation Script
# This script activates the Google traffic blocking

KILLSWITCH_DIR="/usr/local/etc/google-killswitch"
DOMAINS_FILE="$KILLSWITCH_DIR/config/google-domains.txt"
IPS_FILE="$KILLSWITCH_DIR/config/google-ips.txt"
LOG_FILE="/var/log/google-killswitch.log"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Clear existing rules
clear_rules() {
    log "Clearing existing rules..."
    iptables -D OUTPUT -j GOOGLE-BLOCK 2>/dev/null || true
    iptables -F GOOGLE-BLOCK 2>/dev/null || true
    iptables -X GOOGLE-BLOCK 2>/dev/null || true
}

# Create blocking rules
create_rules() {
    log "Creating blocking rules..."
    
    # Create new chain
    iptables -N GOOGLE-BLOCK
    
    # Block domains
    if [[ -f "$DOMAINS_FILE" ]]; then
        while IFS= read -r domain; do
            [[ -n "$domain" && ! "$domain" =~ ^# ]] && iptables -A GOOGLE-BLOCK -d "$domain" -j DROP
        done < "$DOMAINS_FILE"
    fi
    
    # Block IP ranges
    if [[ -f "$IPS_FILE" ]]; then
        while IFS= read -r ip_range; do
            [[ -n "$ip_range" && ! "$ip_range" =~ ^# ]] && iptables -A GOOGLE-BLOCK -d "$ip_range" -j DROP
        done < "$IPS_FILE"
    fi
    
    # Apply chain to OUTPUT
    iptables -A OUTPUT -j GOOGLE-BLOCK
    
    log "Blocking rules activated"
}

# Update hosts file
update_hosts() {
    log "Updating hosts file..."
    cp /etc/hosts /etc/hosts.backup
    
    # Remove existing Google entries
    sed -i '/google\.com/d' /etc/hosts
    
    # Add blocking entries
    if [[ -f "$DOMAINS_FILE" ]]; then
        while IFS= read -r domain; do
            [[ -n "$domain" && ! "$domain" =~ ^# ]] && echo "0.0.0.0 $domain" >> /etc/hosts
        done < "$DOMAINS_FILE"
    fi
    
    log "Hosts file updated"
}

# Main activation
main() {
    log "Activating Google killswitch..."
    
    clear_rules
    create_rules
    update_hosts
    
    log "Google killswitch activation complete"
}

main "$@"
EOF

    chmod +x "$KILLSWITCH_DIR/bin/activate.sh"
    log "Activation script created"
}

# Create deactivation script
create_deactivation_script() {
    log "Creating deactivation script..."
    cat > "$KILLSWITCH_DIR/bin/deactivate.sh" << 'EOF'
#!/bin/bash

# Google Killswitch Deactivation Script
# This script deactivates the Google traffic blocking

KILLSWITCH_DIR="/usr/local/etc/google-killswitch"
LOG_FILE="/var/log/google-killswitch.log"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Clear blocking rules
clear_rules() {
    log "Clearing blocking rules..."
    iptables -D OUTPUT -j GOOGLE-BLOCK 2>/dev/null || true
    iptables -F GOOGLE-BLOCK 2>/dev/null || true
    iptables -X GOOGLE-BLOCK 2>/dev/null || true
    log "Blocking rules cleared"
}

# Restore hosts file
restore_hosts() {
    log "Restoring hosts file..."
    if [[ -f /etc/hosts.backup ]]; then
        mv /etc/hosts.backup /etc/hosts
        log "Hosts file restored"
    else
        log "No backup hosts file found"
    fi
}

# Main deactivation
main() {
    log "Deactivating Google killswitch..."
    
    clear_rules
    restore_hosts
    
    log "Google killswitch deactivation complete"
}

main "$@"
EOF

    chmod +x "$KILLSWITCH_DIR/bin/deactivate.sh"
    log "Deactivation script created"
}

# Create systemd service
create_systemd_service() {
    log "Creating systemd service..."
    cat > "$SERVICE_FILE" << 'EOF'
[Unit]
Description=Google Traffic Killswitch
Documentation=man:google-killswitch(8)
After=network.target
Wants=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/local/etc/google-killswitch/bin/activate.sh
ExecStop=/usr/local/etc/google-killswitch/bin/deactivate.sh
StandardOutput=journal
StandardError=journal
SyslogIdentifier=google-killswitch

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/var/log /usr/local/etc/google-killswitch/logs

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable google-killswitch
    log "Systemd service created and enabled"
}

# Create symbolic links
create_symlinks() {
    log "Creating symbolic links..."
    ln -sf "$KILLSWITCH_DIR/bin/toggle.sh" /usr/local/bin/google-killswitch-toggle
    ln -sf "$KILLSWITCH_DIR/bin/setup-password.sh" /usr/local/bin/google-killswitch-setup
    ln -sf "$KILLSWITCH_DIR/bin/activate.sh" /usr/local/bin/google-killswitch-activate
    ln -sf "$KILLSWITCH_DIR/bin/deactivate.sh" /usr/local/bin/google-killswitch-deactivate
    log "Symbolic links created"
}

# Create monitoring script
create_monitoring_script() {
    log "Creating monitoring script..."
    cat > "$KILLSWITCH_DIR/bin/monitor.sh" << 'EOF'
#!/bin/bash

# Google Killswitch Monitoring Script
# Real-time monitoring of Google traffic attempts

LOG_FILE="/var/log/google-killswitch.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Google Killswitch Monitor${NC}"
echo "=========================="

# Check service status
if systemctl is-active --quiet google-killswitch; then
    echo -e "${GREEN}Status: ACTIVE${NC}"
else
    echo -e "${RED}Status: INACTIVE${NC}"
fi

echo
echo "Recent Google traffic attempts:"
echo "------------------------------"

# Monitor recent blocked attempts
journalctl -u google-killswitch --since "1 hour ago" | grep -i "google\|blocked" | tail -10

echo
echo "Real-time monitoring (Ctrl+C to stop):"
echo "--------------------------------------"

# Real-time monitoring
tcpdump -i any -nn host google.com or host *.google.com 2>/dev/null | while read line; do
    echo -e "${RED}BLOCKED: $line${NC}"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - BLOCKED: $line" >> "$LOG_FILE"
done
EOF

    chmod +x "$KILLSWITCH_DIR/bin/monitor.sh"
    ln -sf "$KILLSWITCH_DIR/bin/monitor.sh" /usr/local/bin/google-killswitch-monitor
    log "Monitoring script created"
}

# Set permissions
set_permissions() {
    log "Setting permissions..."
    chmod -R 755 "$KILLSWITCH_DIR"
    chmod 600 "$KILLSWITCH_DIR/config/"*.txt 2>/dev/null || true
    chown -R root:root "$KILLSWITCH_DIR"
    log "Permissions set"
}

# Main installation function
main() {
    echo -e "${BLUE}Google Killswitch Installation${NC}"
    echo "==============================="
    echo
    
    check_root
    install_dependencies
    create_directories
    create_blocklist
    create_ip_blocklist
    create_password_setup
    create_toggle_script
    create_activation_script
    create_deactivation_script
    create_systemd_service
    create_symlinks
    create_monitoring_script
    set_permissions
    
    echo
    echo -e "${GREEN}Installation completed successfully!${NC}"
    echo
    echo "Next steps:"
    echo "1. Set up password: sudo google-killswitch-setup"
    echo "2. Activate killswitch: sudo systemctl start google-killswitch"
    echo "3. Toggle status: google-killswitch-toggle"
    echo "4. Monitor traffic: google-killswitch-monitor"
    echo
    echo "Log file: $LOG_FILE"
    echo "Configuration: $KILLSWITCH_DIR"
}

# Run main function
main "$@"
EOF

chmod +x google_killswitch_implementation.sh
log "Google killswitch implementation script created"