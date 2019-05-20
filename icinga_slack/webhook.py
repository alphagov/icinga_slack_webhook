#!/usr/bin/env python3

import argparse
import json
import urllib.parse
import urllib.request
import sys

from icinga_slack import __version__

alert_colors = {'UNKNOWN': '#6600CC',
                'CRITICAL': '#FF0000',
                'WARNING': '#FF9900',
                'OK': '#36A64F'}

def abbreviate_url(url):
    parsed_url = urllib.parse.urlparse(url)

    return "<{0}|{1}>".format(url, parsed_url.netloc)

class AttachmentField(dict):
    def __init__(self, title, value, short=False):
        self['title'] = title
        self['value'] = value
        self['short'] = short


class AttachmentFieldList(list):
    def __init__(self, *args):
        for count, field in enumerate(args):
            self.append(field)


class Attachment(dict):
    def __init__(self, fallback, fields, text=None, pretext=None, color=None):
        self['fallback'] = fallback
        self['fields'] = fields
        if text:
            self['text'] = text
        if pretext:
            self['pretext'] = pretext
        if color:
            self['color'] = color


class AttachmentList(list):
    def __init__(self, *args):
        for count, attachment in enumerate(args):
            self.append(attachment)


class Message(dict):
    def __init__(self, channel, text, username, mrkdwn_in=["fields"],
                 icon_emoji=":ghost:", attachments=None):
        self['channel'] = channel
        self['text'] = text
        if mrkdwn_in:
            self['mrkdwn_in'] = mrkdwn_in
        if username:
            self['username'] = username
        if icon_emoji:
            self['icon_emoji'] = icon_emoji
        self['attachments'] = AttachmentList()

    def attach(
            self,
            message,
            host,
            level,
            action_url=None,
            notes_url=None,
            status_cgi_url=''
    ):
        fields = AttachmentFieldList()
        fields.append(
            AttachmentField(
                "Host",
                abbreviate_url("{0}?host={1}".format(status_cgi_url, host)),
                True
            )
        )
        fields.append(AttachmentField("Level", level, True))
        if action_url:
            fields.append(AttachmentField("Actions URL", action_url, True))
        if notes_url:
            fields.append(AttachmentField("Notes URL", notes_url, True))
        if level in alert_colors.keys():
            color = alert_colors[level]
        else:
            color = alert_colors['UNKNOWN']
        alert_attachment = Attachment(
            fallback="    {0} on {1} is {2}".format(message, host, level),
            color=color,
            fields=fields
        )
        self['attachments'].append(alert_attachment)

    def send(self, webhook_url):
        data = urllib.parse.urlencode({"payload": json.dumps(self)})
        response = urllib.request.urlopen(
            webhook_url,
            data.encode('utf8')
        ).read()
        if response == b'ok':
            return True
        else:
            print("Error: %s" % response)
            return False


def parse_options():
    parser = argparse.ArgumentParser(
        prog="icinga_slack_webhook_notify",
        description="Send an Icinga Alert to Slack.com via a generic webhook integration"
    )
    parser.add_argument(
        '-c', '--channel',
        required=True,
        help="The channel to send the message to"
    )
    parser.add_argument(
        '-m', '--message',
        required=True,
        help="The text of the message to send"
    )
    destination_group = parser.add_mutually_exclusive_group()
    destination_group.add_argument(
        '-u', '--web-hook-url',
        help="The webhook URL for your integration"
    )
    destination_group.add_argument(
        '-p', '--print-payload',
        action='store_const',
        const=True,
        default=False,
        help="Rather than sending the payload to Slack, print it to STDOUT"
    )
    parser.add_argument(
        '-A', '--service-action-url',
        default=None,
        help="An optional action_url for this alert {default: None}"
    )
    parser.add_argument(
        '-H', '--host',
        default="UNKNOWN",
        help="An optional host the message relates to {default: UNKNOWN}"
    )
    parser.add_argument(
        '-L', '--level',
        choices=["OK", "WARNING", "CRITICAL", "UNKNOWN"],
        default="UNKNOWN",
        help="An optional alert level {default: UNKNOWN}"
    )
    parser.add_argument(
        '-N', '--service-notes-url',
        default=None,
        help="An optional notes_url for this alert {default: None}"
    )
    parser.add_argument(
        '-S', '--status-cgi-url',
        default='https://nagios.example.com/cgi-bin/icinga/status.cgi',
        help="The URL of status.cgi for your Nagios/Icinga instance {default: https://nagios.example.com/cgi-bin/icinga/status.cgi}"
    )
    parser.add_argument(
        '-U', '--username',
        default="Icinga",
        help="Username to send the message from {default: Icinga}"
    )
    parser.add_argument(
        '-V', '--version',
        action='version',
        help="Print version information",
        version=__version__
    )

    return parser.parse_args()


def main():
    args = parse_options()
    message = Message(
        channel=args.channel, text=args.message, username=args.username
    )
    message.attach(
        message=args.message,
        host=args.host,
        level=args.level,
        action_url=args.service_action_url,
        notes_url=args.service_notes_url,
        status_cgi_url=args.status_cgi_url
    )

    if args.print_payload:
        print(json.dumps(message, indent=True))
    else:
        if message.send(webhook_url=args.web_hook_url):
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
