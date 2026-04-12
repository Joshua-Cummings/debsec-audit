#!/usr/bin/env python3
import argparse
import subprocess
import os
from datetime import datetime

class colors:
    HIGH = "\033[91m"
    MEDIUM = "\033[93m"
    LOW = "\033[94m"
    SAFE = "\033[92m"
    RESET = "\033[0m"

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception: {str(e)}"

def check_packages():
    print("Checking for upgradable packages...")
    return run_command("apt list --upgradable 2>/dev/null | tail -n +2")

def check_permissions():
    print("Scanning for world-writable files in /etc...")
    return run_command("find /etc -type f -perm -002 2>/dev/null | head -10")

def check_network():
    print("Checking listening network ports...")
    return run_command("ss -tuln 2>/dev/null || netstat -tuln 2>/dev/null")

def main():
    parser = argparse.ArgumentParser(description="Basic Debian Security Auditor CLI")
    parser.add_argument("--check", choices=["packages", "permissions", "network", "all"], default="all", help="Specific check to run")
    parser.add_argument("--output", type=str, help="Save report to file")
    args = parser.parse_args()

    report = [f"Debian Security Audit Report - {datetime.now()}\n"]

    if args.check in ["packages", "all"]:
        report.append("=== Packages Check ===\n")
        package_results = check_packages()
        if package_results:
            report.append(f"{colors.HIGH}HIGH SEVERITY - Updates Missing:\n\n" + package_results + f"{colors.RESET}\n")
        else:
            report.append(f"{colors.SAFE} - No Updates Available{colors.RESET}\n")
    if args.check in ["permissions", "all"]:
        report.append("=== Permissions Check ===\n")
        permission_results = check_permissions()
        if permission_results:
            report.append(f"{colors.LOW}LOW SEVERITY - Risky Permissions:\n\n" + permission_results + f"{colors.RESET}\n")
        else:
            report.append(f"{colors.SAFE} - No Risky Permissions Found{colors.RESET}\n")
    if args.check in ["network", "all"]:
        report.append("=== Network Check ===\n")
        network_results = check_network()
        if network_results:
            report.append(f"{colors.MEDIUM}MEDIUM SEVERITY - Ports Opened:\n\n" + network_results + f"{colors.RESET}\n")
        else:
            report.append(f"{colors.SAFE} - No Ports Open{colors.RESET}\n")

    output = "\n".join(report)
    print(output)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report saved to {args.output}")

if __name__ == "__main__":
    main()
