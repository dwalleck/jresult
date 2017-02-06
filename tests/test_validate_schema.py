from jsonschema import ValidationError

from xunitjson import validate_schema, xunitjson_schema



valid_result = {
    "testsuites":
        {
            "tests": "1",
            "errors": "0",
            "skips": "0",
            "time": "0.007",
            "failures": "0"
        },
    "testcases": [
        {
            "classname": "demo_tests",
            "name": "test_capability",
            "time": "0.5"
        }
    ]
}


def test_validate_schema():
    validate_schema.validate(valid_result, xunitjson_schema.schema)


def test_validate_invalid_schema_fails():
    invalid_result = valid_result.copy()
    del invalid_result['testsuites']
    
    try:
        validate_schema.validate(invalid_result, xunitjson_schema.schema)
    except ValidationError as ex:
        # This is the expected path
        assert ex.message == "'testsuites' is a required property"
    else:
        assert False