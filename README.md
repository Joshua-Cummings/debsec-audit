# debsec-audit

**A lightweight command-line security auditor for Debian-based systems.**

Quickly scan for upgradable packages, world-writable files, listenting ports, and other common misconfigurations. Built as a hobby project to practice Python CLI development and security tooling.

## Features
- Check for upgradable packages
- Scan for insecure file permissions
- List listening network services
- Simple text report output (with future JSON support planned)
- Runs safely on local Debian systems

## Installation / Quick Start

```bash
git clone https://github.com/Joshua-Cummings/debsec-audit.git
cd debsec-audit
python3 -m venv venv
source venv/bin/activate
chmod +x debsec_audit.py
```

## Usage

```bash
./debsec_audit.py --help
./debsec_audit.py # Run all checks
./debsec_audit.py --check packages
./debsec_audit.py --check permissions --output report.txt
./debsec_audit.py --check network --verbose
```

## Project Goals

This tool serves as a foundation for building more advanced auditing, incident response, and red teaming utilities in Python (with planned Rust components for performance-critical parts).

## Development Setup
- Python 3.10+
- Only uses the standard library (no external dependencies yet)
- Virtual environment recommended

## Roadmap
- Add severity ratings and color output
- JSON export for integration with other tools
- More checks (user accounts, SSH config, etc.)
- Packaging for easy installation

## License

MIT
