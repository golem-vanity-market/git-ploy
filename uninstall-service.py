import os
import subprocess
from os import environ


repository_path = environ.get("GITPLOY_REPOSITORY_ROOT", ".")
p = os.path.abspath(repository_path)
repository_name = environ.get("GITPLOY_REPOSITORY_NAME", os.path.basename(p))

service_name = f"{repository_name}-gitploy.service"
service_location = f"/etc/systemd/system/{service_name}"


if hasattr(os, "geteuid") and os.geteuid() != 0:
    print("Please run this script with sudo.")
    raise SystemExit(1)


def run(command):
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


print(f"Uninstalling autoupdater service: {service_name}")

print("Stopping service if it exists...")
run(["systemctl", "stop", service_name])

print("Disabling service if it exists...")
run(["systemctl", "disable", service_name])

if os.path.exists(service_location):
    os.remove(service_location)
    print(f"Removed service file: {service_location}")
else:
    print(f"Service file not found: {service_location}")

print("Reloading systemd daemon...")
run(["systemctl", "daemon-reload"])

print("Resetting failed service state...")
run(["systemctl", "reset-failed", service_name])

print("Autoupdater service uninstalled.")
