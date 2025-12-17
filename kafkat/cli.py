"""Command line interface for Kafkat."""

import json
import sys
from typing import List, Optional
import click
from .config import Config
from .consumer import KafkatConsumer
from .logger import setup_logging, get_logger
from .exceptions import KafkatError
from . import __version__


def validate_bootstrap_servers(ctx, param, value):
    """Validate bootstrap servers format."""
    if not value:
        return value
    
    servers = value.split(',')
    for server in servers:
        if ':' not in server:
            raise click.BadParameter(f"Invalid server format: {server}. Expected format: host:port")
    return value


@click.command()
@click.option(
    '-b', '--bootstrap-server',
    default=None,
    callback=validate_bootstrap_servers,
    help='Bootstrap servers (comma-separated)'
)
@click.option(
    '-c/-C', '--auto-commit/--no-auto-commit',
    default=None,
    help='Enable/disable autocommit'
)
@click.option(
    '-o', '--auto-offset-reset',
    type=click.Choice(['earliest', 'latest', 'none']),
    default=None,
    help='Auto offset reset strategy'
)
@click.option(
    '-e', '--separator',
    default=None,
    help='Field separator for output'
)
@click.option(
    '-p/-P', '--prettify/--no-prettify',
    default=None,
    help='Prettify JSON output'
)
@click.option(
    '-t', '--topic',
    multiple=True,
    help='Topic patterns to search (can be specified multiple times)'
)
@click.option(
    '-s', '--search',
    default='.*',
    help='Search pattern (regex)'
)
@click.option(
    '-m', '--max-messages',
    type=int,
    default=None,
    help='Maximum number of messages to process'
)
@click.option(
    '--timeout',
    type=int,
    default=None,
    help='Consumer timeout in seconds'
)
@click.option(
    '-v', '--verbose',
    is_flag=True,
    help='Enable verbose logging'
)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Suppress all output except errors'
)
@click.option(
    '--config-show',
    is_flag=True,
    help='Show current configuration and exit'
)
@click.option(
    '--config-reset',
    is_flag=True,
    help='Reset configuration to defaults'
)
@click.option(
    '--list-topics',
    is_flag=True,
    help='List all available topics matching pattern and exit'
)
@click.version_option(version=__version__, prog_name='kafkat')
def main(
    bootstrap_server: Optional[str],
    auto_commit: Optional[bool],
    auto_offset_reset: Optional[str],
    separator: Optional[str],
    prettify: Optional[bool],
    topic: tuple,
    search: str,
    max_messages: Optional[int],
    timeout: Optional[int],
    verbose: bool,
    quiet: bool,
    config_show: bool,
    config_reset: bool,
    list_topics: bool
):
    """Kafkat - A powerful Kafka search CLI tool.
    
    Search for messages in Kafka topics using regex patterns.
    
    Examples:
    
    \b
    # Search for order ID in multiple topics
    kafkat --search '.*982834084219' -t 'orders.*' -t 'payments.*' --prettify
    
    \b
    # List all topics matching pattern
    kafkat --list-topics -t 'user.*'
    
    \b
    # Search with custom bootstrap servers
    kafkat -b localhost:9092,localhost:9093 -s 'error' -t 'logs.*'
    """
    
    # Setup logging
    logger = setup_logging(verbose=verbose, quiet=quiet)
    
    # Load configuration
    config = Config()
    
    # Handle config commands
    if config_show:
        _show_config(config)
        return
    
    if config_reset:
        _reset_config(config)
        return
    
    # Update config with CLI options
    _update_config_from_cli(
        config, bootstrap_server, auto_commit, auto_offset_reset,
        separator, prettify, max_messages, timeout
    )
    
    try:
        # Create consumer
        consumer = KafkatConsumer(
            bootstrap_servers=config.get('bootstrap_servers'),
            auto_offset_reset=config.get('auto_offset_reset'),
            consumer_timeout_ms=config.get('consumer_timeout_ms'),
            auto_commit=config.get('auto_commit')
        )
        
        # Get topics
        topics = _get_topics(consumer, topic, config)
        
        if list_topics:
            _list_topics(topics)
            return
        
        if not topics:
            logger.error("No topics found matching the specified patterns")
            sys.exit(1)
        
        # Perform search
        _search_messages(
            consumer, topics, search, config, logger
        )
        
    except KafkatError as e:
        logger.error(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Search interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        try:
            consumer.close()
        except:
            pass


def _show_config(config: Config):
    """Show current configuration."""
    click.echo("Current Kafkat Configuration:")
    click.echo("=" * 30)
    for key, value in config.to_dict().items():
        click.echo(f"{key:20}: {value}")


def _reset_config(config: Config):
    """Reset configuration to defaults."""
    config._config = config.DEFAULT_CONFIG.copy()
    config.save_config()
    click.echo("Configuration reset to defaults")


def _update_config_from_cli(
    config: Config,
    bootstrap_server: Optional[str],
    auto_commit: Optional[bool],
    auto_offset_reset: Optional[str],
    separator: Optional[str],
    prettify: Optional[bool],
    max_messages: Optional[int],
    timeout: Optional[int]
):
    """Update configuration with CLI options."""
    updates = {}
    
    if bootstrap_server is not None:
        updates['bootstrap_servers'] = bootstrap_server
    if auto_commit is not None:
        updates['auto_commit'] = auto_commit
    if auto_offset_reset is not None:
        updates['auto_offset_reset'] = auto_offset_reset
    if separator is not None:
        updates['separator'] = separator
    if prettify is not None:
        updates['prettify'] = prettify
    if max_messages is not None:
        updates['max_messages'] = max_messages
    if timeout is not None:
        updates['consumer_timeout_ms'] = timeout * 1000
    
    if updates:
        config.update(**updates)
        config.save_config()


def _get_topics(consumer: KafkatConsumer, topic_patterns: tuple, config: Config) -> List[str]:
    """Get list of topics to search."""
    if not topic_patterns:
        topic_patterns = ('.*',)
    
    all_topics = set()
    for pattern in topic_patterns:
        topics = consumer.get_topics(pattern)
        all_topics.update(topics)
    
    return list(all_topics)


def _list_topics(topics: List[str]):
    """List available topics."""
    if not topics:
        click.echo("No topics found")
        return
    
    click.echo(f"Found {len(topics)} topics:")
    for topic in topics:
        click.echo(f"  {topic}")


def _search_messages(
    consumer: KafkatConsumer,
    topics: List[str],
    search_pattern: str,
    config: Config,
    logger
):
    """Search for messages and output results."""
    max_messages = config.get('max_messages', 1000)
    prettify = config.get('prettify', False)
    
    # Show progress
    if not config.get('quiet', False):
        logger.info(f"Starting search in {len(topics)} topics...")
        click.echo(f"Searching for pattern '{search_pattern}' in topics: {', '.join(topics)}", err=True)
    
    found_any = False
    try:
        for message in consumer.search_messages(topics, search_pattern, max_messages):
            found_any = True
            _output_message(message, prettify)
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise
    
    if not found_any and not config.get('quiet', False):
        logger.info("No messages found matching the search criteria")


def _output_message(message: dict, prettify: bool):
    """Output a single message."""
    if prettify:
        output = json.dumps(message, indent=2, ensure_ascii=False)
    else:
        output = json.dumps(message, ensure_ascii=False)
    
    click.echo(output)


if __name__ == '__main__':
    main()
