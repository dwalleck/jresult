import argparse
import json
import sys
from xml.etree import ElementTree


def convert_results(result_data):
    # Developed against the accepted jUnit XML spec:
    # https://github.com/windyroad/JUnit-Schema/blob/master/JUnit.xsd
    element = ElementTree.parse(result_data).getroot()
    result_summary = {item[0]: item[1] for item in element.items()}

    test_results = element.findall('testcase')

    results = []
    for result in test_results:
        partial_result = {result[0]: result[1] for result in result.items()}
        # If there are error or failure entries, add them as well
        for test_error in result.getchildren():
            partial_result[test_error.tag] = test_error.text
        results.append(partial_result)

    final_result = {
        'testsuites': result_summary,
        'testcases': results
    }

    return final_result


def entry_point():
    parser = argparse.ArgumentParser(description='junitxml2xunitjson')

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
    final_results = convert_results(args.input, args.result_file)
    output_file = open(args.result_file, 'w+')
    json.dump(final_result, output_file)
