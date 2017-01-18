import argparse
import json
import sys
from xml.etree import ElementTree


def convert_results(result_data, result_file):
    # Developed against the accepted jUnit XML spec:
    # https://github.com/windyroad/JUnit-Schema/blob/master/JUnit.xsd
    element = ElementTree.parse(result_data).getroot()
    result_summary = {item[0]: item[1] for item in element.items()}

    test_results = element.findall('testcase')

    results = []
    for result in test_results:
        results.append({result[0]: result[1] for result in result.items()})

    final_result = {
        'testsuites': result_summary,
        'testcases': results
    }

    output_file = open(result_file, 'w+')
    json.dump(final_result, output_file)


def entry_point():
    parser = argparse.ArgumentParser(description='junitxml2jresult')

    parser.add_argument(
        'input',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin
    )

    parser.add_argument(
        '-o', action='store',
        dest='result_file',
        default='results.json'
    )

    args = parser.parse_args()
    convert_results(args.input, args.result_file)
