import uuid

from xunitjson import xunitjson2splunk


test_run_id = str(uuid.uuid4())

successful_result = {
        'classname': 'test_class',
        'name': 'first_test',
        'time': '5.0'
}

result_with_error = successful_result.copy()
result_with_error['error'] = 'stack trace'

result_with_failure = successful_result.copy()
result_with_failure['failure'] = 'test failure'


def test_denormalize_xunitjson_result_success():
    result = xunitjson2splunk.denormalize_xunitjson_result(
        test_run_id, successful_result)
    assert result['test_run_id'] == test_run_id
    assert result['test_name'] == 'first_test'
    assert result['test_classname'] == 'test_class'
    assert result['test_result'] == 'pass'
    assert result['reason'] == None
    assert result['duration'] == '5.0'


def test_denormalize_xunitjson_result_failure():
    result = xunitjson2splunk.denormalize_xunitjson_result(
        test_run_id, result_with_failure)
    assert result['test_run_id'] == test_run_id
    assert result['test_name'] == 'first_test'
    assert result['test_classname'] == 'test_class'
    assert result['test_result'] == 'fail'
    assert result['reason'] == result_with_failure['failure']
    assert result['duration'] == '5.0'


def test_convert_denormalize_xunitjson_result_error():
    result = xunitjson2splunk.denormalize_xunitjson_result(
        test_run_id, result_with_error)
    assert result['test_run_id'] == test_run_id
    assert result['test_name'] == 'first_test'
    assert result['test_classname'] == 'test_class'
    assert result['test_result'] == 'error'
    assert result['reason'] == result_with_error['error']
    assert result['duration'] == '5.0'