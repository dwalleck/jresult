import argparse
import json
import sys

from jsonschema import validate, ValidationError

from xunitjson_schema import schema


def entry_point():
    parser = argparse.ArgumentParser(description='junitxml2xunitjson')
    parser.add_argument(
        'input',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin
    )
    args = parser.parse_args()

    try:
        validate(json.loads(args.input.read()), schema)
    except ValidationError as e:
        print 'xunitjson validation failed: {message}'.format(
            message=e.message)
        sys.exit(1)
    else:
        print 'Validation successful.'
        sys.exit(0)