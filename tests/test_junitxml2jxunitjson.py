from xunitjson import junitxml2xunitjson

from six import StringIO 


def test_convert_results_with_test_success():
    xml_result = '<testsuite errors="0" failures="0" skips="0" tests="1" time="0.007"><testcase classname="demo_tests" name="test_capability" time="0.001"></testcase></testsuite>'
    result_file = StringIO(xml_result)
    converted_results = junitxml2xunitjson.convert_results(result_file)
    
    assert converted_results['testsuites']['errors'] == '0'
    assert converted_results['testsuites']['failures'] == '0'
    assert converted_results['testsuites']['skips'] == '0'
    assert converted_results['testsuites']['tests'] == '1'
    assert converted_results['testsuites']['time'] == '0.007'

    assert len(converted_results['testcases']) == 1
    converted_result = converted_results['testcases'][0]
    assert converted_result['classname'] == 'demo_tests'
    assert converted_result['name'] == 'test_capability'
    assert converted_result['time'] == '0.001'
    assert converted_result.get('failure') is None
    assert converted_result.get('error') is None


def test_convert_results_with_test_failure():
    xml_result = '<testsuite errors="0" failures="1" skips="0" tests="1" time="0.007"><testcase classname="demo_tests" name="test_capability" time="0.001"><failure>Failure to launch</failure></testcase></testsuite>'
    result_file = StringIO(xml_result)
    converted_results = junitxml2xunitjson.convert_results(result_file)
    
    assert converted_results['testsuites']['errors'] == '0'
    assert converted_results['testsuites']['failures'] == '1'
    assert converted_results['testsuites']['skips'] == '0'
    assert converted_results['testsuites']['tests'] == '1'
    assert converted_results['testsuites']['time'] == '0.007'

    assert len(converted_results['testcases']) == 1
    converted_result = converted_results['testcases'][0]
    assert converted_result['classname'] == 'demo_tests'
    assert converted_result['name'] == 'test_capability'
    assert converted_result['time'] == '0.001'
    assert converted_result['failure'] == 'Failure to launch'


def test_convert_results_with_test_error():
    xml_result = '<testsuite errors="1" failures="0" skips="0" tests="1" time="0.007"><testcase classname="demo_tests" name="test_capability" time="0.000"><error>Stack trace</error></testcase></testsuite>'
    result_file = StringIO(xml_result)
    converted_results = junitxml2xunitjson.convert_results(result_file)
    
    assert converted_results['testsuites']['errors'] == '1'
    assert converted_results['testsuites']['failures'] == '0'
    assert converted_results['testsuites']['skips'] == '0'
    assert converted_results['testsuites']['tests'] == '1'
    assert converted_results['testsuites']['time'] == '0.007'

    assert len(converted_results['testcases']) == 1
    converted_result = converted_results['testcases'][0]
    assert converted_result['classname'] == 'demo_tests'
    assert converted_result['name'] == 'test_capability'
    assert converted_result['time'] == '0.000'
    assert converted_result['error'] == 'Stack trace'