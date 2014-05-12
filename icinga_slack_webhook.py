#!/usr/bin/env python

import argparse
import json
import urllib
import sys

alert_colors = {'UNKNOWN': '#6600CC',
                'CRITICAL': '#FF0000',
                'WARNING': '#FF9900',
                'OK': '#00FF00'}


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
    def __init__(self, channel, text='Received the following alert:', mrkdwn_in=["fields"], username="Icinga",
                 icon_emoji=":ghost:", attachments=None):
        self['channel'] = channel
        self['text'] = text
        if mrkdwn_in:
            self['mrkdwn_in'] = mrkdwn_in
        if username:
            self['username'] = username
        if icon_emoji:
            self['icon_emoji'] = icon_emoji

    def attach(self, message, host, level, action_url=None, notes_url=None):
        fields = AttachmentFieldList()
        fields.append(AttachmentField("Message", message))
        fields.append(AttachmentField("Host", "<https://nagios.example.com/cgi-bin/icinga/status.cgi?host={0}|{0}>".format(host), True))
        fields.append(AttachmentField("Level", level, True))
        if action_url:
            fields.append(AttachmentField("Actions URL", action_url, True))
        if notes_url:
            fields.append(AttachmentField("Notes URL", notes_url, True))
        if level in alert_colors.keys():
            color = alert_colors[level]
        else:
            color = alert_colors['UNKNOWN']
        alert_attachment = Attachment(fallback="    {0} on {1} is {2}".format(message, host, level), color=color, fields=fields)
        self['attachments'] = AttachmentList(alert_attachment)

    def send(self, subdomain, token):
        data = urllib.urlencode({"payload": json.dumps(self)})
        response = urllib.urlopen('https://{0}.slack.com/services/hooks/incoming-webhook?token={1}'.format(subdomain, token), data).read()
        if response == "ok":
            return True
        else:
            print "Error: %s" % response
            return False


def parse_options():
    parser = argparse.ArgumentParser(description="Send an Icinga Alert to Slack.com")
    parser.add_argument('-s', metavar="SUBDOMAIN", type=str, required=True)
    parser.add_argument('-t', metavar="TOKEN", type=str, required=True)
    parser.add_argument('-c', metavar="CHANNEL", type=str, required=True)
    parser.add_argument('-m', metavar="MESSAGE", type=str, required=True)
    parser.add_argument('-H', metavar="HOST", type=str, default="UNKNOWN")
    parser.add_argument('-l', metavar="LEVEL", type=str, choices=["OK", "WARNING", "CRITICAL", "UNKNOWN"], default="UNKNOWN")
    parser.add_argument('-A', metavar="SERVICEACTIONURL", type=str, default=None)
    parser.add_argument('-N', metavar="SERVICENOTESURL", type=str, default=None)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_options()
    message = Message(channel=args.c)
    message.attach(message=args.m, host=args.H, level=args.l, action_url=args.A, notes_url=args.N)
    if message.send(subdomain=args.s, token=args.t):
        sys.exit(0)
    else:
        sys.exit(1)
