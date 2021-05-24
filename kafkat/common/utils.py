import json


def decode_value(value):
    try:
        return json.loads(value.decode('utf-8'))
    except Exception as e:
        return {'error': str(e)}


def prettify_json(value):
    return json.dumps(value, indent=4, sort_keys=True)
