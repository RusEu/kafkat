"""Kafka consumer functionality."""

import json
import re
import signal
import sys
from typing import List, Dict, Any, Optional, Iterator, Pattern
from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError
from .logger import get_logger
from .exceptions import ConnectionError, SearchError


class KafkatConsumer:
    """Enhanced Kafka consumer for searching messages."""
    
    def __init__(
        self,
        bootstrap_servers: str,
        auto_offset_reset: str = 'earliest',
        consumer_timeout_ms: int = 5000,
        auto_commit: bool = True,
        **kwargs
    ):
        self.logger = get_logger(__name__)
        self.bootstrap_servers = bootstrap_servers
        self.consumer_config = {
            'bootstrap_servers': bootstrap_servers.split(','),
            'auto_offset_reset': auto_offset_reset,
            'consumer_timeout_ms': consumer_timeout_ms,
            'enable_auto_commit': auto_commit,
            'value_deserializer': lambda x: x.decode('utf-8', errors='ignore'),
            'key_deserializer': lambda x: x.decode('utf-8', errors='ignore') if x else None,
            **kwargs
        }
        self.consumer = None
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(sig, frame):
            self.logger.info("Received interrupt signal, shutting down gracefully...")
            if self.consumer:
                self.consumer.close()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def connect(self) -> None:
        """Establish connection to Kafka."""
        try:
            self.logger.debug(f"Connecting to Kafka at {self.bootstrap_servers}")
            self.consumer = KafkaConsumer(**self.consumer_config)
            self.logger.info("Connected to Kafka successfully")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Kafka: {str(e)}")
    
    def get_topics(self, pattern: str = '.*') -> List[str]:
        """Get list of topics matching pattern."""
        if not self.consumer:
            self.connect()
        
        try:
            topic_regex = re.compile(pattern)
            all_topics = self.consumer.list_consumer_group_offsets()
            metadata = self.consumer.list_consumer_groups()
            
            # Get all available topics
            topics_metadata = self.consumer.topics()
            matching_topics = [topic for topic in topics_metadata if topic_regex.match(topic)]
            
            self.logger.info(f"Found {len(matching_topics)} topics matching pattern '{pattern}'")
            return sorted(matching_topics)
            
        except Exception as e:
            self.logger.error(f"Failed to get topics: {str(e)}")
            return []
    
    def search_messages(
        self,
        topics: List[str],
        search_pattern: str,
        max_messages: int = 1000,
        timeout_seconds: int = 10
    ) -> Iterator[Dict[str, Any]]:
        """Search for messages matching pattern in specified topics."""
        if not self.consumer:
            self.connect()
        
        if not topics:
            self.logger.warning("No topics specified for search")
            return
        
        try:
            search_regex = re.compile(search_pattern, re.IGNORECASE)
        except re.error as e:
            raise SearchError(f"Invalid search pattern: {str(e)}")
        
        self.logger.info(f"Searching in topics: {', '.join(topics)}")
        self.logger.info(f"Search pattern: {search_pattern}")
        
        try:
            # Subscribe to topics
            self.consumer.subscribe(topics)
            
            message_count = 0
            found_count = 0
            
            # Poll for messages
            while message_count < max_messages:
                message_batch = self.consumer.poll(timeout_ms=1000)
                
                if not message_batch:
                    continue
                
                for topic_partition, messages in message_batch.items():
                    for message in messages:
                        message_count += 1
                        
                        # Create message info
                        message_info = {
                            'topic': message.topic,
                            'partition': message.partition,
                            'offset': message.offset,
                            'timestamp': message.timestamp,
                            'key': message.key,
                            'value': message.value
                        }
                        
                        # Search in message value
                        if self._matches_pattern(message.value, search_regex):
                            found_count += 1
                            yield self._format_message(message_info)
                        
                        # Search in message key if it exists
                        elif message.key and self._matches_pattern(message.key, search_regex):
                            found_count += 1
                            yield self._format_message(message_info)
                        
                        if message_count >= max_messages:
                            break
                    
                    if message_count >= max_messages:
                        break
            
            self.logger.info(f"Search completed. Found {found_count} matches out of {message_count} messages")
            
        except KafkaError as e:
            raise SearchError(f"Kafka error during search: {str(e)}")
        except Exception as e:
            raise SearchError(f"Unexpected error during search: {str(e)}")
    
    def _matches_pattern(self, text: str, pattern: Pattern) -> bool:
        """Check if text matches the search pattern."""
        if not text:
            return False
        
        return pattern.search(text) is not None
    
    def _format_message(self, message_info: Dict[str, Any]) -> Dict[str, Any]:
        """Format message for output."""
        formatted = {
            'topic': message_info['topic'],
            'partition': message_info['partition'],
            'offset': message_info['offset']
        }
        
        if message_info['timestamp']:
            from datetime import datetime
            formatted['timestamp'] = datetime.fromtimestamp(
                message_info['timestamp'] / 1000
            ).isoformat()
        
        if message_info['key']:
            formatted['key'] = message_info['key']
        
        # Try to parse value as JSON
        try:
            formatted['value'] = json.loads(message_info['value'])
        except (json.JSONDecodeError, TypeError):
            formatted['value'] = message_info['value']
        
        return formatted
    
    def close(self):
        """Close the consumer connection."""
        if self.consumer:
            self.consumer.close()
            self.logger.info("Kafka consumer closed")
