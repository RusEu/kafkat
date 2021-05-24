# Kafkat

![Python Logo](https://www.python.org/static/community_logos/python-logo.png "Python logo")


This is a simple Python application intended to provide a way to search for data in kafka.


## How to use it



Command:

`$ kafkat --help`

```
Options:
  -b, --bootstrap-server TEXT   Bootstrap servers  [default: 0.0.0.0:9092]
  -c, --auto-commit             Enable autocommit  [default: True]
  -o, --auto-offset-reset TEXT  Auto offset reset  [default: earliest]
  -e, --separator TEXT          Separator  [default: ,]
  -p, --prettify                Prettify Json Output.  [default: False]
  -t, --topic TEXT              Topic Pattern  [default: .*]
  -s, --search TEXT             Search Pattern  [default: .*]
  --help                        Show this message and exit.
```

----

Command:

`$ kafkat --search '.*982834084219' -t 'topic_1.*' -t 'topic_2.*' -t 'topic_3.*'  --prettify`

```json
{
    "order": "982834084219",
    "updatedAt": "2021-05-24T17:06:34.267Z",
},
{
    "order": "982834084219",
    "updatedAt": "2021-05-24T17:06:34.267Z",
},
```

