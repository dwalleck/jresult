import os
import sys
from setuptools import setup, find_packages

setup(
    name='xunitjson',
    version='0.0.1',
    description='A proposal for an alternate JSON unit test result format',
    long_description='{0}'.format(open('README.md').read()),
    author='Daryl Walleck',
    author_email='dwalleck@gmail.com',
    url='https://github.com/dwalleck/xunitjson',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
    entry_points={
        'console_scripts':
        ['junitxml2xunitjson = xunitjson.junitxml2xunitjson:entry_point',
         'validate-xunitjson = xunitjson.validate_schema:entry_point',
         'xunitjson2splunk = xunitjson.xunitjson2splunk:entry_point',
         'xunitjson2httpcollector = xunitjson.xunitjson2splunk:http_collector_entry_point']})
