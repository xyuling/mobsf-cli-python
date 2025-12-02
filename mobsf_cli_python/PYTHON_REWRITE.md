# Python Rewrite of mobsf-cli

This document describes the Python rewrite of the original Rust mobsf-cli project.

## Overview

The mobsf-cli tool has been completely rewritten in Python while maintaining full feature parity with the original Rust implementation. The Python version provides the same command-line interface, functionality, and behavior.

## Project Structure

### Original Rust Structure
```
mobsf-cli/
├── mobsf-core/          # Core library crate
│   └── src/
│       ├── lib.rs       # Main API client
│       ├── error.rs     # Error types
│       └── response.rs  # Response models
├── mobsf-cli/           # CLI binary crate
│   └── src/
│       ├── main.rs      # Entry point
│       ├── app.rs       # Application logic
│       ├── cli.rs       # Argument parsing
│       └── error.rs     # CLI errors
└── Cargo.toml           # Workspace config
```

### New Python Structure
```
mobsf_cli_python/
├── mobsf_core/          # Core API client module
│   ├── __init__.py
│   ├── client.py        # Main API client
│   ├── error.py         # Error handling
│   └── response.py      # Response models
├── cli/                 # CLI interface module
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── app.py           # Application logic
│   ├── arguments.py     # Argument parsing
│   └── error.py         # CLI error handling
├── tests/               # Unit tests
├── setup.py             # Installation config
├── pyproject.toml       # Project metadata
└── requirements.txt     # Dependencies
```

## Feature Comparison

| Feature | Rust | Python | Status |
|---------|------|--------|--------|
| Upload files | ✅ | ✅ | Complete |
| Scan files | ✅ | ✅ | Complete |
| List scans | ✅ | ✅ | Complete |
| PDF reports | ✅ | ✅ | Complete |
| JSON reports | ✅ | ✅ | Complete |
| Delete scans | ✅ | ✅ | Complete |
| View source | ✅ | ✅ | Complete |
| Play mode | ✅ | ✅ | Complete |
| CI/CD mode | ✅ | ✅ | Complete |
| Environment vars | ✅ | ✅ | Complete |
| CLI overrides | ✅ | ✅ | Complete |
| Table output | ✅ | ✅ | Complete |
| Error handling | ✅ | ✅ | Complete |

## Dependencies

### Rust Dependencies
- `reqwest` - HTTP client
- `serde` - Serialization
- `cli-table` - Table formatting
- `chrono` - Date/time handling
- `clap` - Argument parsing
- `tokio` - Async runtime

### Python Dependencies
- `requests` - HTTP client
- `tabulate` - Table formatting
- `python-dateutil` - Date/time handling
- Built-in `argparse` - Argument parsing

## Implementation Details

### API Client (mobsf_core)

#### Rust (lib.rs)
- Uses `reqwest` async HTTP client
- Manual error conversion with custom types
- Async/await with tokio runtime
- Streaming file uploads and downloads

#### Python (client.py)
- Uses `requests` synchronous HTTP client
- Exception-based error handling
- Synchronous I/O
- Chunked file transfers

### Error Handling

#### Rust (error.rs)
```rust
pub enum Cause {
    HttpClientError,
    IoError,
    InvalidHttpResponse(u16),
}

pub struct MobsfError {
    pub cause: Cause,
    pub message: String,
}
```

#### Python (error.py)
```python
class ErrorCause(Enum):
    HTTP_CLIENT_ERROR = "HttpClientError"
    IO_ERROR = "IoError"
    INVALID_HTTP_RESPONSE = "InvalidHttpResponse"

class MobsfError(Exception):
    def __init__(self, cause: ErrorCause, message: str, status_code: Optional[int] = None)
```

### Response Models

Both implementations use data classes/structs with:
- Type-safe field definitions
- JSON deserialization
- Display/formatting implementations
- Builder methods

#### Rust uses:
- `#[derive(Debug, Deserialize)]`
- Manual `Display` trait implementations
- `cli-table` procedural macros

#### Python uses:
- `@dataclass` decorator
- `__str__` methods
- `tabulate` for table formatting

### CLI Interface

#### Rust (cli.rs)
- Uses `clap` v3 with builder pattern
- Subcommands with nested options
- Compile-time validation

#### Python (arguments.py)
- Uses `argparse` standard library
- Subparsers for commands
- Runtime validation

## Usage Examples

All commands work identically in both versions:

```bash
# Upload
mobsf-cli upload app.apk

# Scan
mobsf-cli scan apk app.apk abc123

# Play (upload + scan)
mobsf-cli play app.apk

# Reports
mobsf-cli report pdf abc123 -o report.pdf
mobsf-cli report json abc123 -p

# List scans
mobsf-cli scans

# CI/CD
mobsf-cli ci app.apk -p ./reports -c 5.0 -u 70 -t 5

# Delete
mobsf-cli delete abc123

# View source
mobsf-cli source apk MainActivity.java abc123
```

## Advantages of Python Version

1. **Easy Installation**: No compilation required, works on any system with Python
2. **Readable**: Python's syntax is more accessible to non-Rust developers
3. **Debugging**: Easier to debug and trace issues
4. **Integration**: Simpler to integrate with Python-based CI/CD tools
5. **Dependencies**: Fewer and simpler dependencies
6. **Development**: Faster iteration and modification

## Advantages of Rust Version

1. **Performance**: Faster execution, especially for large files
2. **Binary**: Single compiled binary with no runtime dependencies
3. **Memory Safety**: Compile-time guarantees
4. **Concurrency**: Better async performance
5. **Type Safety**: Stronger compile-time checks

## Testing

### Running Tests

```bash
# Python
cd mobsf_cli_python
pytest tests/

# Rust
cd mobsf-cli
cargo test
```

## Installation

### Python
```bash
cd mobsf_cli_python
pip install -e .
mobsf-cli --help
```

### Rust
```bash
cd mobsf-cli
cargo build --release
./target/release/mobsf-cli --help
```

## Compatibility

Both versions:
- Use the same MobSF REST API endpoints
- Accept identical command-line arguments
- Produce compatible output
- Support the same environment variables
- Can be used interchangeably in CI/CD pipelines

## Migration Guide

If you're currently using the Rust version and want to switch to Python:

1. Install Python version: `pip install -e mobsf_cli_python/`
2. The command name remains the same: `mobsf-cli`
3. All scripts and CI/CD configurations work without changes
4. Environment variables work identically
5. Output formats are compatible

## Conclusion

The Python rewrite successfully maintains feature parity with the Rust implementation while providing the benefits of Python's ecosystem and ease of use. The choice between versions depends on your specific requirements:

- Choose **Python** for easier integration, development, and maintenance
- Choose **Rust** for maximum performance and standalone binary distribution

Both versions are production-ready and can be used based on your team's preferences and requirements.
