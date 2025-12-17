# Kafkat

![Python Logo](https://www.python.org/static/community_logos/python-logo.png "Python logo")

[![PyPI version](https://badge.fury.io/py/kafkat.svg)](https://badge.fury.io/py/kafkat)
[![Python Support](https://img.shields.io/pypi/pyversions/kafkat.svg)](https://pypi.org/project/kafkat/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Kafkat is a powerful Python CLI tool for searching and analyzing data in Apache Kafka topics. It provides an intuitive interface for real-time message searching with regex patterns, topic filtering, and flexible output formatting.

## Features

- 🔍 **Regex Search**: Search messages using powerful regex patterns
- 📋 **Topic Filtering**: Search across multiple topics with pattern matching
- 🎨 **Pretty Output**: JSON formatting with syntax highlighting
- ⚙️ **Configuration**: Persistent configuration management
- 📊 **Progress Tracking**: Real-time search progress indicators
- 🚀 **Performance**: Efficient message processing with configurable limits
- 🔧 **Flexible**: Extensive CLI options for customization
- 📝 **Logging**: Configurable logging with multiple verbosity levels

## Installation

### From PyPI (Recommended)

```bash
pip install kafkat
```

### From Source

```bash
git clone https://github.com/danielrus/kafkat.git
cd kafkat
pip install -e .
```

## Quick Start

### Basic Usage

```bash
# Search for a specific pattern in all topics
kafkat --search "error" 

# Search in specific topics with pretty output
kafkat --search "order_id.*12345" -t "orders.*" -t "payments.*" --prettify

# List available topics
kafkat --list-topics -t "user.*"
```

### Configuration

```bash
# Show current configuration
kafkat --config-show

# Reset configuration to defaults
kafkat --config-reset
```

## Command Reference

### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--bootstrap-server` | `-b` | Kafka bootstrap servers (comma-separated) | `localhost:9092` |
| `--auto-commit/--no-auto-commit` | `-c/-C` | Enable/disable auto commit | `True` |
| `--auto-offset-reset` | `-o` | Offset reset strategy | `earliest` |
| `--separator` | `-e` | Field separator for output | `,` |
| `--prettify/--no-prettify` | `-p/-P` | Pretty print JSON output | `False` |
| `--topic` | `-t` | Topic patterns (multiple allowed) | `.*` |
| `--search` | `-s` | Search regex pattern | `.*` |
| `--max-messages` | `-m` | Maximum messages to process | `1000` |
| `--timeout` | | Consumer timeout in seconds | `10` |
| `--verbose` | `-v` | Enable verbose logging | `False` |
| `--quiet` | `-q` | Suppress non-error output | `False` |
| `--list-topics` | | List matching topics and exit | `False` |
| `--config-show` | | Show current configuration | `False` |
| `--config-reset` | | Reset configuration to defaults | `False` |
| `--version` | | Show version and exit | |
| `--help` | | Show help message | |

### Examples

#### Search for Specific Order ID

```bash
kafkat --search '.*982834084219' -t 'orders.*' -t 'payments.*' --prettify
```

**Output:**
```json
{
  "topic": "orders.processed",
  "partition": 0,
  "offset": 12345,
  "timestamp": "2023-12-07T10:30:45.123Z",
  "value": {
    "order_id": "982834084219",
    "status": "processed",
    "amount": 99.99
  }
}
```

#### Search for Errors with Custom Bootstrap Server

```bash
kafkat -b "kafka1:9092,kafka2:9092" --search "ERROR|FATAL" -t "logs.*" --max-messages 500
```

#### List All User-Related Topics

```bash
kafkat --list-topics -t "user.*" -t "profile.*"
```

**Output:**
```
Found 5 topics:
  user.created
  user.updated
  user.deleted
  profile.events
  profile.changes
```

#### Search with Verbose Logging

```bash
kafkat --search "payment.*failed" -t "transactions.*" --verbose
```

## Configuration

Kafkat stores configuration in `~/.kafkat/config.json`. You can modify settings using CLI options, and they will be persisted for future use.

### Default Configuration

```json
{
  "bootstrap_servers": "localhost:9092",
  "auto_commit": true,
  "auto_offset_reset": "earliest",
  "separator": ",",
  "prettify": false,
  "timeout_ms": 10000,
  "max_messages": 1000,
  "consumer_timeout_ms": 5000
}
```

## Advanced Usage

### Environment Variables

You can set environment variables to override default settings:

```bash
export KAFKAT_BOOTSTRAP_SERVERS="kafka1:9092,kafka2:9092"
export KAFKAT_AUTO_OFFSET_RESET="latest"
kafkat --search "error"
```

### Regex Patterns

Kafkat supports full Python regex syntax for powerful searching:

```bash
# Case-insensitive search
kafkat --search "(?i)error"

# Search for JSON field
kafkat --search '"status":\s*"failed"'

# Search for IP addresses
kafkat --search '\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# Search for UUIDs
kafkat --search '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
```

### Output Formatting

Control output format based on your needs:

```bash
# Compact JSON (one line per message)
kafkat --search "order" --no-prettify

# Pretty formatted JSON
kafkat --search "order" --prettify

# Quiet mode (errors only)
kafkat --search "order" --quiet
```

## Performance Tips

1. **Limit Message Count**: Use `--max-messages` to prevent processing too many messages
2. **Specific Topics**: Use specific topic patterns instead of `.*` for better performance
3. **Efficient Patterns**: Use specific regex patterns rather than broad ones
4. **Timeout Settings**: Adjust `--timeout` based on your Kafka cluster performance

## Error Handling

Kafkat provides detailed error messages and proper exit codes:

- `0`: Success
- `1`: General error (connection, search, etc.)
- `130`: Interrupted by user (Ctrl+C)

### Common Issues

#### Connection Problems

```bash
# Test connectivity
kafkat --list-topics --verbose

# Use specific bootstrap servers
kafkat -b "your-kafka-server:9092" --list-topics
```

#### No Messages Found

```bash
# Check if topics exist
kafkat --list-topics -t "your-pattern"

# Try different offset reset
kafkat --search "pattern" --auto-offset-reset latest
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/danielrus/kafkat.git
cd kafkat
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black kafkat/
flake8 kafkat/
mypy kafkat/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v2.0.0
- Complete rewrite with improved architecture
- Added configuration management
- Enhanced error handling and logging
- Better CLI interface with more options
- Improved search performance
- Added progress indicators
- Signal handling for graceful shutdown

### v1.0.0
- Initial release
- Basic search functionality
- Simple CLI interface

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/danielrus/kafkat/issues) page
2. Create a new issue with detailed information
3. Include logs with `--verbose` flag for debugging

---

**Author**: Daniel Rus  
**Email**: dani@fsck.ro  
**License**: MIT
