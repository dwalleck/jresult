import argparse
import json
import sys
import uuid

from jsonschema import validate, ValidationError

from jresult_schema import schema
from splunklib import client


def convert_jresult_to_normalized_result(test_run_id, result):
    test_result = None
    reason = None

    if result.get('error'):
        test_result = 'error'
        reason = result['error']
    elif result.get('failure'):
        test_result = 'fail'
        reason = result['fail']
    else:
        test_result = 'pass'
    
    normalized_result = {
        'test_run_id': test_run_id,
        'test_name': result['name'],
        'test_classname': result['classname'],
        'test_result': test_result,
        'reason': reason,
        'duration': result['time'],
    }
    return normalized_result


def save_results(results, host, port, username, password, index):
    
    # Verify we can connect with Splunk
    service = client.connect(
        host=host,
        port=port,
        username=username,
        password=password
    )

    # Write each individual result to Splunk
    test_run_id = str(uuid.uuid4())
    for result in results['testcases']:
        normalized_result = convert_jresult_to_normalized_result(
            test_run_id, result)
        service.indexes[index].submit(json.dumps(result)

def entry_point():
    parser = argparse.ArgumentParser(description='jresult2splunk')

    parser.add_argument(
        'input',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin
    )

    parser.add_argument(
        '--host', action='store',
        dest='host',
        default='localhost'
    )

    parser.add_argument(
        '--port', action='store',
        dest='port',
        default='8089'
    )

    parser.add_argument(
        '-u', action='store',
        dest='username',
        default='admin'
    )

    parser.add_argument(
        '-p', action='store',
        dest='password',
    )

    parser.add_argument(
        '-i', action='store',
        dest='index',
        default='test_results'
    )

    args = parser.parse_args()

    # Validate the input file before further processing
    results = json.loads(args.input.read())
    validate(results, schema)

    save_results(
        results,
        args.host,
        args.port,
        args.username,
        args.password,
        args.index)
