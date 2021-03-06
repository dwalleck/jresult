import argparse
import json
import sys
import uuid

from jsonschema import validate, ValidationError
import requests

from xunitjson_schema import schema
from splunklib import client


def denormalize_xunitjson_result(test_run_id, result):
    test_result = None
    reason = None

    if result.get('error'):
        test_result = 'error'
        reason = result['error']
    elif result.get('failure'):
        test_result = 'fail'
        reason = result['failure']
    else:
        test_result = 'pass'
    
    denormalized_result = {
        'test_run_id': test_run_id,
        'test_name': str(result['name']),
        'test_classname': str(result['classname']),
        'test_result': test_result,
        'reason': reason or '',
        'duration': str(result['time']),
    }
    return denormalized_result


def save_results_to_splunk(results, host, port, username, password, index):
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
        normalized_result = denormalize_xunitjson_result(
            test_run_id, result)
        service.indexes[index].submit(json.dumps(result))


def send_results_to_splunk_http_collector(results, host, port, token):
    headers = {'Authorization': 'Splunk {token}'.format(token=token),
               'Content-Type': 'application/json'}
    test_run_id = str(uuid.uuid4())
    for result in results['testcases']:
        normalized_result = denormalize_xunitjson_result(
            test_run_id, result)
        splunk_data = {
            'sourcetype': 'xunitjson',
            'event': normalized_result
        }
        response = requests.post(
            'https://{host}:{port}/services/collector'.format(host=host, port=port),
            headers=headers,
            data=json.dumps(splunk_data),
            verify=False)


def entry_point():
    parser = argparse.ArgumentParser(description='xunitjson2splunk')

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

    save_results_to_splunk(
        results,
        args.host,
        args.port,
        args.username,
        args.password,
        args.index)


def http_collector_entry_point():
    parser = argparse.ArgumentParser(description='xunitjson2httpcollector')

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
        default='8088'
    )

    parser.add_argument(
        '-t', action='store',
        dest='token'
    )

    args = parser.parse_args()

    # Validate the input file before further processing
    results = json.loads(args.input.read())
    validate(results, schema)
    send_results_to_splunk_http_collector(results, args.host, args.port, args.token)