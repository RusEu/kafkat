import re

import click
from kafka import KafkaConsumer

from .common.utils import decode_value, prettify_json


@click.command()
@click.option('-b', '--bootstrap-server', help='Bootstrap servers',
              default=['0.0.0.0:9092'], multiple=True, show_default=True)
@click.option('-c', '--auto-commit', help='Enables autocommit',
              default=True, type=bool, is_flag=True, show_default=True)
@click.option('-o', '--auto-offset-reset', help='Auto offset reset',
              default='earliest', show_default=True)
@click.option('-e', '--separator', help='Separator',
              default=',', show_default=True)
@click.option('-p', '--prettify', help='Prettify Json Output.',
              default=False, type=bool, is_flag=True, show_default=True)
@click.option('-t', '--topic', help="Topic Pattern",
              multiple=True, default='.*', show_default=True)
@click.option('-s', '--search', help="Search Pattern",
              default='.*', show_default=True)
def kafkat(bootstrap_server, auto_commit, auto_offset_reset,
           separator, prettify, topic, search):

    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_server,
        auto_offset_reset=auto_offset_reset,
        enable_auto_commit=auto_commit,
        value_deserializer=decode_value
    )

    consumer.subscribe(pattern='|'.join(topic))

    pattern = re.compile(search, re.DOTALL)

    for message in consumer:
        value = message.value

        if prettify:
            value = prettify_json(value)

        if separator:
            value = f'{value}{separator}'

        if re.match(pattern, value):
            click.echo(value)
