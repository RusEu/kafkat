"""Kafkat - A powerful Kafka search CLI tool.

Kafkat is a command-line interface tool designed to search and analyze Apache Kafka
topics efficiently. It provides advanced search capabilities, filtering options,
and real-time monitoring of Kafka message streams.

Key Features:
- Search messages across Kafka topics with flexible filtering
- Support for various message formats and serialization
- Real-time streaming and batch processing modes
- Export capabilities for search results
- User-friendly CLI interface with comprehensive options

Example:
    $ kafkat search --topic my-topic --filter "field:value"
    $ kafkat list-topics --bootstrap-server localhost:9092

For more information, visit: https://github.com/danielrus/kafkat
"""

__version__ = "2.0.0"
__author__ = "Daniel Rus"
__email__ = "dani@fsck.ro"
