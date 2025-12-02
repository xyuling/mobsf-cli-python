# mobsf-cli (Python Version)

mobsf-cli is a Python wrapper for the Mobile Security Framework (MobSF) REST-API. Created especially for Continuous Integration (CI) / Continuous Delivery (CD) stages. You can use only one command to upload a file, auto start scan, save reports, and check scores.

[Mobile Security Framework (MobSF)](https://github.com/MobSF/Mobile-Security-Framework-MobSF) is an automated, all-in-one mobile application (Android/iOS/Windows) pen-testing, malware analysis and security assessment framework capable of performing static and dynamic analysis.

## Features

- 🚀 Simple CLI interface for MobSF operations
- 📦 Upload and scan mobile apps (APK, IPA, APPX, etc.)
- 📊 Generate PDF and JSON reports
- 🔍 View scan results and source files
- ✅ Automated security validation for CI/CD pipelines
- 🐍 Pure Python implementation with minimal dependencies

## Installation

### From Source

```bash
git clone https://github.com/wojciech-zurek/mobsf-cli.git
cd mobsf-cli/mobsf_cli_python
pip install -e .
```

### Using pip (after publishing)

```bash
pip install mobsf-cli
```

### Requirements

- Python 3.8 or higher
- requests >= 2.28.0
- tabulate >= 0.9.0
- python-dateutil >= 2.8.0

## Usage

```bash
mobsf-cli [OPTIONS] <COMMAND>

OPTIONS:
    -a API_KEY      Api key/token (overrides MOBSF_API_KEY env)
    -s SERVER       Server, example: http://localhost:8000 (overrides MOBSF_SERVER env)
    -h, --help      Show help message
    --version       Show version information

COMMANDS:
    ci        For CI/CD stages. Upload a file, auto start scan, save reports, check scores.
    delete    Delete scan.
    play      Upload a file and auto start scan.
    report    Get report (pdf or json).
    scan      Scan a file.
    scans     Display recent scans.
    source    View source files.
    upload    Upload a file.
```

### Example Usage

```bash
# Upload a file to MobSF server
mobsf-cli upload path/to/example.apk

# Scan a file
mobsf-cli scan apk example.apk <hash>

# Upload a file and auto start scan
mobsf-cli play path/to/example.apk

# Fetch scan result (report)
mobsf-cli report pdf <hash>
mobsf-cli report json <hash>

# Display recent scans
mobsf-cli scans

# Delete scan result
mobsf-cli delete <hash>
```

## CI/CD Usage

`mobsf-cli ci` combines:

- Upload a file
- Start scan
- Generate reports in PDF and JSON format
- Check scan scores (CVSS, security score, trackers) and raise an error if scores are wrong

```bash
# Help
mobsf-cli ci --help

mobsf-cli ci [OPTIONS] FILE_PATH

ARGUMENTS:
    FILE_PATH    Path to the file to scan

OPTIONS:
    -p PATH_TO_SAVE          Path to directory to save reports (pdf and json) [required]
    -r                       Rescan a file
    -c CVSS                  Above this score raise a cvss error. 0.0-10.0 [default: 3.9]
    -t TRACKERS              Above this score raise a trackers error. 0-407 [default: 0]
    -u SECURITY              Below this score raise a security error. 0-100 [default: 71]
```

### Example CI/CD Usage

```bash
mobsf-cli ci path/to/example.apk -p path/to/save/reports -c 5.5 -u 48 -t 2
```

Output:
```
...
Validating scan scores...
Error: CVSS score [6.6] is too high. Max: 5.5!
```

## Server and API Key Configuration

You can set server and api key:

- As command options (higher priority):
  - `-a <api_key>`
  - `-s <server>`
- As environment variables (lower priority)

### Environment Variables

You can set environment variables for API and server configuration:

- `MOBSF_API_KEY` - for api key
- `MOBSF_SERVER` - for server URL

```bash
export MOBSF_API_KEY="ed...c4"
export MOBSF_SERVER="https://su...com:8000"
mobsf-cli scans
```

Or inline:

```bash
MOBSF_API_KEY="ed...c4" MOBSF_SERVER="https://su...com:8000" mobsf-cli scans
```

## Project Structure

```
mobsf_cli_python/
├── mobsf_core/          # Core MobSF API client
│   ├── __init__.py
│   ├── client.py        # Main API client
│   ├── error.py         # Error handling
│   └── response.py      # Response models
├── cli/                 # CLI interface
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── app.py           # Application logic
│   ├── arguments.py     # Argument parser
│   └── error.py         # CLI error handling
├── tests/               # Tests
├── setup.py             # Setup configuration
├── pyproject.toml       # Project metadata
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines. You can check code style with:

```bash
flake8 mobsf_core cli
black mobsf_core cli --check
```

### Type Checking

```bash
mypy mobsf_core cli
```

## Differences from Rust Version

This Python version maintains feature parity with the original Rust implementation:

- ✅ All commands and options are identical
- ✅ Same API endpoints and behavior
- ✅ Compatible output formats
- ✅ Environment variable support
- 🐍 Python-idiomatic code structure
- 📦 Easy to install and integrate

## License

MIT License - see LICENSE file for details

## Author

Wojciech Zurek <mail@wojciechzurek.eu>

Python port maintains the same interface and functionality as the original Rust version.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- [MobSF GitHub](https://github.com/MobSF/Mobile-Security-Framework-MobSF)
- [MobSF API Documentation](https://mobsf.github.io/Mobile-Security-Framework-MobSF/rest_api.html)
- [Original Rust Version](https://github.com/wojciech-zurek/mobsf-cli)
