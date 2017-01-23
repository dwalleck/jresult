import os
import sys
from setuptools import setup, find_packages

setup(
    name='jresult',
    version='0.0.1',
    description='A proposal for an alternate JSON unit test result format',
    long_description='{0}'.format(open('README.md').read()),
    author='Daryl Walleck',
    author_email='dwalleck@gmail.com',
    url='https://github.com/dwalleck/jresult',
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
        ['junitxml2jresult = jresult.junitxml2jresult:entry_point',
         'validate-jresult = jresult.validate_schema:entry_point',
         'jresult2splunk = jresult.jresult2splunk:entry_point']})