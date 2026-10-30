#!/usr/bin/env bash
# pi_projects/ops/harden.sh — run once on a fresh Raspberry Pi OS install
set -euo pipefail

# 1. Patching: unattended security updates
sudo apt-get install -y unattended-upgrades apt-listchanges
sudo dpkg-reconfigure -f noninteractive unattended-upgrades

# 2. SSH: keys only, no root, restricted users
sudo tee /etc/ssh/sshd_config.d/10-hardening.conf >/dev/null <<'EOF'
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
AllowGroups ssh-users
MaxAuthTries 3
EOF
sudo groupadd -f ssh-users && sudo usermod -aG ssh-users "$USER"
sudo systemctl reload ssh

# 3. Firewall: deny inbound except SSH from the management subnet
sudo apt-get install -y ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 192.168.10.0/24 to any port 22 proto tcp
sudo ufw --force enable

# 4. Brute-force protection
sudo apt-get install -y fail2ban

# 5. Local AI services listen on loopback only
sudo mkdir -p /etc/systemd/system/ollama.service.d
printf '[Service]\nEnvironment="OLLAMA_HOST=127.0.0.1:11434"\n' | \
  sudo tee /etc/systemd/system/ollama.service.d/override.conf >/dev/null
sudo systemctl daemon-reload && sudo systemctl restart ollama

# 6. Dedicated, unprivileged service account for AI apps
sudo useradd --system --create-home --shell /usr/sbin/nologin assistant || true
sudo usermod -aG audio,video,gpio assistant

# 7. Disable what you do not use
sudo systemctl disable --now bluetooth.service cups.service 2>/dev/null || true

echo "Baseline applied. Remember: change the management subnet above to yours."
