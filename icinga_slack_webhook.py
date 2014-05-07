#!/usr/bin/env python

import argparse
import json
import urllib
import sys

class AttachmentField(dict):
    def __init__(self, title, value, short = False):
        self['title'] = title
        self['value'] = value
        self['short'] = short

class AttachmentFieldList(list):
    def __init__(self, *args):
        for count, field in enumerate(args):
            self.append(field)

class Attachment(dict):
    def __init__(self, fallback, fields, text = None, pretext = None, color = None):
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

class Payload(dict):
    def __init__(self, channel, text, mrkdwn_in = None, username = None, icon_emoji = None, attachments = None):
        self['channel'] = channel
        self['text'] = text
        if mrkdwn_in:
            self['mrkdwn_in'] = mrkdwn_in
        if username:
            self['username'] = username
        if icon_emoji:
            self['icon_emoji'] = icon_emoji
        if attachments:
            self['attachments'] = attachments

def format_alert_attachment_list(message, host, level, action_url = None, notes_url = None):
    fields = AttachmentFieldList()
    fields.append(AttachmentField("Message", message))
    fields.append(AttachmentField("Host", "<https://nagios.example.com/cgi-bin/icinga/status.cgi?host={0}|{0}>".format(host), True))
    fields.append(AttachmentField("Level", level, True))
    if action_url:
        fields.append(AttachmentField("Actions URL", action_url, True))
    if notes_url:
        fields.append(AttachmentField("Notes URL", notes_url, True ))

    if level == "CRITICAL":
        color = "#FF0000"
    elif level == "WARNING":
        color = "#FF6600"
    elif level == "OK":
        color = "#00FF00"
    else:
        color = "#6600CC"

    alert_attachment = Attachment(fallback = "    {0} on {1} is {2}".format(message, host, level), color = color, fields = fields)
    return AttachmentList(alert_attachment)

def create_url_payload(channel, message, host, level, action_url = None, notes_url = None):
    payload = Payload( channel = channel,
                       text = 'Service status message received:',
                       mrkdwn_in = [ "fields" ],
                       username = "Icinga",
                       icon_emoji = ":ghost:",
                       attachments = format_alert_attachment_list(message, host, level, action_url, notes_url))
    data = urllib.urlencode({"payload": json.dumps(payload)})
    return data

def send_slack_message(subdomain, token, channel, message, host, level, action_url = None, notes_url = None):
    data = create_url_payload(channel, message, host, level, action_url, notes_url)
    response = urllib.urlopen('https://{0}.slack.com/services/hooks/incoming-webhook?token={1}'.format(subdomain, token), data).read()
    if response == "ok":
        return True
    else:
        print "Error: %s" % response
        return False

def parse_options():
    parser = argparse.ArgumentParser(description="Send an Icinga Alert to Slack.com")
    parser.add_argument('-s', metavar = "SUBDOMAIN", type=str, required=True)
    parser.add_argument('-t', metavar = "TOKEN", type=str, required=True)
    parser.add_argument('-c', metavar = "CHANNEL", type=str, required=True)
    parser.add_argument('-m', metavar = "MESSAGE", type=str, required=True)
    parser.add_argument('-H', metavar = "HOST", type=str, default="UNKNOWN")
    parser.add_argument('-l', metavar = "LEVEL", type=str, choices=["OK","WARNING","CRITICAL","UNKNOWN"], default="UNKNOWN")
    parser.add_argument('-A', metavar = "SERVICEACTIONURL", type=str, default=None)
    parser.add_argument('-N', metavar = "SERVICENOTESURL", type=str, default=None)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_options()
    if send_slack_message(subdomain = args.s, token = args.t, channel = args.c, message = args.m, host = args.H, level = args.l, action_url = args.A, notes_url = args.N):
        sys.exit(0)
    else:
        sys.exit(1)
