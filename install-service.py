import os.path
import time
from os import environ

repository_path = environ.get("GITPLOY_REPOSITORY_ROOT", ".")
p = os.path.abspath(repository_path)
repository_name = environ.get("GITPLOY_REPOSITORY_NAME", os.path.basename(p))
USER_TO_INSTALL_SERVICE = environ.get("GITPLOY_USER", "ubuntu")

print(f"Downloading the latest gitploy.py to {p}...")
os.system("curl -H 'Cache-Control: no-cache' -sSL https://raw.githubusercontent.com/golem-vanity-market/git-ploy/refs/heads/main/gitploy.py --output gitploy.py")

SERVICE_LOCATION = f"/etc/systemd/system/{repository_name}-gitploy.service"
print(f"Repository root to install service: {p}")

print("Stopping service if exists...")
os.system(f"sudo systemctl stop {repository_name}-gitploy.service")
print("Disable service if exists...")
os.system(f"sudo systemctl disable {repository_name}-gitploy.service")


service_content = f"""
# Service installed from https://raw.githubusercontent.com/golem-vanity-market/git-ploy

[Unit]
Description=Autoupdate service for {repository_name}
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory={p}
ExecStart=/usr/bin/python3 -u gitploy.py
Restart=on-failure
RestartSec=120
# Allow sudo to elevate, only use these settings in administrative scripts
NoNewPrivileges=no
ProtectSystem=off
ProtectHome=off
PrivateTmp=no

[Install]
WantedBy=multi-user.target
"""

with open(SERVICE_LOCATION, "w") as f:
    f.write(service_content)

print(f"Service file written to {SERVICE_LOCATION}")

print("Reloading systemd daemon...")
os.system("sudo systemctl daemon-reload")
print("Enabling the autoupdate service...")
os.system(f"sudo systemctl enable {repository_name}-gitploy.service")
print("Starting the autoupdate service...")
os.system(f"sudo systemctl start {repository_name}-gitploy.service")

time.sleep(1)

os.system(f"sudo systemctl status {repository_name}-gitploy.service")

print(f"Run: journalctl -u {repository_name}-gitploy.service -f to see the service logs.")

print("To check if autoupdater works correctly run: git reset --hard HEAD^ (warning to not lost changes)")