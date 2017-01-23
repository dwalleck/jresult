testcase_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'error': {'type': 'integer'},
        'failure': {'type': 'integer'},
        'classname': {'type': 'string'},
        'time': {'type': 'string'},
    },
    'additionalProperties': True,
    'required': ['name', 'classname', 'time']
}

# TODO: The keys for testsuites should be required. Need to add to schema
schema = {
    'type': 'object',
    'properties': {
        'testsuites': {
            'type': 'object',
            'properties': {
                'errors': {'type': 'string'},
                'failures': {'type': 'string'},
                'name': {'type': 'string'},
                'skips': {'type': 'string'},
                'tests': {'type': 'string'},
                'time': {'type': 'string'}
                
            }
        },
        'testcases': {
            'type': 'array',
            'items': testcase_schema
        }
    },
    'additionalProperties': True,
    'required': ['testsuites', 'testcases']
}

