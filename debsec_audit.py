#!/usr/bin/env python3
import argparse
import subprocess
import os
from datetime import datetime

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
        report.append("=== Package Check ===\n" + check_packages() + "\n")
    if args.check in ["permissions", "all"]:
        report.append("=== Permissions Check ===\n" + check_permissions() + "\n")
    if args.check in ["network", "all"]:
        report.append("=== Network Check ===\n" + check_network() + "\n")

    output = "\n".join(report)
    print(output)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report saved to {args.output}")

if __name__ == "__main__":
    main()
