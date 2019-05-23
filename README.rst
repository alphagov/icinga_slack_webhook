icinga-slack-webhook
====================

A script to send notifications to Slack.com from Nagios or Icinga via the generic webhook integration

.. image:: https://travis-ci.org/alphagov/icinga_slack_webhook.png?branch=master
   :target: https://travis-ci.org/alphagov/icinga_slack_webhook

The `homepage is on Github <https://github.com/alphagov/icinga_slack_webhook>`_

Installation
------------

    $ pip install icinga-slack-webhook

Usage
-----

::

    usage: icinga_slack_webhook_notify [-h] -c CHANNEL -m MESSAGE [-u WEB_HOOK_URL | -p]
                                       [-A SERVICE_ACTION_URL] [-H HOST] [-d HOST_DISPLAY_NAME]
                                       [--host-state HOST_STATE]
                                       [-L {OK,WARNING,CRITICAL,UNKNOWN}] [-N SERVICE_NOTES_URL]
                                       [-S STATUS_CGI_URL] [-E EXTINFO_CGI_URL] [-U USERNAME]
                                       [-V]

    Send an Icinga Alert to Slack.com via a generic webhook integration

    optional arguments:
      -h, --help            show this help message and exit
      -c CHANNEL, --channel CHANNEL
                            The channel to send the message to
      -m MESSAGE, --message MESSAGE
                            The text of the message to send
      -u WEB_HOOK_URL, --web-hook-url WEB_HOOK_URL
                            The webhook URL for your integration
      -p, --print-payload   Rather than sending the payload to Slack, print it to STDOUT
      -A SERVICE_ACTION_URL, --service-action-url SERVICE_ACTION_URL
                            An optional action_url for this alert {default: None}
      -H HOST, --host HOST  An optional host the message relates to
      -d HOST_DISPLAY_NAME, --host-display-name HOST_DISPLAY_NAME
                            An optional display name for the host the message relates to
      --host-state HOST_STATE
                            An optional state the host is in, use this for host alerts
      -L {OK,WARNING,CRITICAL,UNKNOWN}, --level {OK,WARNING,CRITICAL,UNKNOWN}
                            An optional alert level {default: UNKNOWN}
      -N SERVICE_NOTES_URL, --service-notes-url SERVICE_NOTES_URL
                            An optional notes_url for this alert {default: None}
      -S STATUS_CGI_URL, --status-cgi-url STATUS_CGI_URL
                            The URL of status.cgi for your Nagios/Icinga instance {default:
                            https://nagios.example.com/cgi-bin/icinga/status.cgi}
      -E EXTINFO_CGI_URL, --extinfo-cgi-url EXTINFO_CGI_URL
                            The URL of extinfo.cgi for your Nagios/Icinga instance
      -U USERNAME, --username USERNAME
                            Username to send the message from {default: Icinga}
      -V, --version         Print version information
