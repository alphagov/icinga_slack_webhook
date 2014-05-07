#!/usr/bin/env python

from distutils.core import setup

setup(name='icinga_slack_webhook',
      version='0.1.0',
      description='Script to send from Icinga (or Nagios) to Slack via an Incoming Webhook',
      author='Sam Sharpe',
      author_email='sam.sharpe@gmail.com',
      url='https://github.com/samjsharpe/icinga_slack_webhook',
      packages=['distutils', 'distutils.command'],
     )
