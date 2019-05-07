#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

from icinga_slack import __version__

repo_directory = os.path.dirname(__file__)
try:
    long_description = open(os.path.join(repo_directory, 'README.rst')).read()
except:
    long_description = None

setup(
    name='icinga-slack-webhook',
    version=__version__,
    packages=find_packages(exclude=['test*']),

    author='Sam Sharpe',
    author_email='sam.sharpe@digital.cabinet-office.gov.uk',
    maintainer='Sam Sharpe',
    url='https://github.com/samjsharpe/icinga_slack_webhook',

    description='icinga-slack-webhook: A notifier from Icinga to Slack',
    long_description=long_description,
    license='MIT',
    keywords='',

    setup_requires=['setuptools-pep8'],

    tests_require=[
        "nose==1.3.3"
    ],

    test_suite='nose.collector',

    entry_points={
        'console_scripts': [
            'icinga_slack_webhook_notify=icinga_slack.webhook:main'
        ]
    }
)
