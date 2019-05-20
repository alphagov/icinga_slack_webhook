import unittest

from icinga_slack.webhook import AttachmentField, AttachmentFieldList, Attachment, AttachmentList, Message

class TestCommon(unittest.TestCase):

    def setUp(self):
        self.example_attachment_field = {"title": "My Title", "value": "My Value"}
        self.example_attachment_field2 = {"title": "My Second Title", "value": "My Second Value", "short": True}
        self.example_attachment_field_list = [self.example_attachment_field]
        self.example_attachment_field_list2 = [self.example_attachment_field, self.example_attachment_field2]
        self.example_attachment = {"fallback": "Fallback Message", "fields": self.example_attachment_field_list, "test": "Example Text", "pretext": "Example pretext", "color": "#FF0000"}

class TestAttachmentField(TestCommon):

    def setUp(self):
        self.attachment_field = AttachmentField("My Title", "My Value")
        self.attachment_field_optional = AttachmentField("My Second Title", "My Second Value", True)

    def test_attachment_field_required_attributes(self):
        self.assertTrue('title' in self.attachment_field.keys())
        self.assertTrue('value' in self.attachment_field.keys())
        self.assertTrue('short' in self.attachment_field.keys())

    def test_attachment_field_optional_defaults(self):
        self.assertFalse(self.attachment_field['short'])
        self.assertTrue(self.attachment_field_optional['short'])


class TestAttachmentFieldList(TestCommon):

    def test_creating_one_field_attachment_list(self):
        self.attachment_list = AttachmentFieldList(self.example_attachment_field)
        self.assertEqual(len(self.attachment_list), 1)

    def test_creating_two_field_attachment_list(self):
        self.attachment_list = AttachmentFieldList(self.example_attachment_field, self.example_attachment_field2)
        self.assertEqual(len(self.attachment_list), 2)
        self.assertEqual(self.attachment_list[1]["value"], "My Second Value")


class TestAttachment(TestCommon):

    def test_attachment_with_defaults(self):
        self.attachment = Attachment("Fallback Message", self.example_attachment_field_list)
        self.assertEqual(self.attachment['fallback'], "Fallback Message")
        self.assertEqual(self.attachment['fields'], self.example_attachment_field_list )

    def test_attachment_with_optionals(self):
        self.attachment = Attachment("Fallback Message", self.example_attachment_field_list, [], "Text", "Pretext", "#FF0000")
        self.assertEqual(self.attachment['text'], "Text")
        self.assertEqual(self.attachment['pretext'], "Pretext")
        self.assertEqual(self.attachment['color'], "#FF0000")

class TestAttachmentList(TestCommon):

    def test_single_attachment_list(self):
        self.attachment_list = AttachmentList(self.example_attachment)
        self.assertEqual(len(self.attachment_list), 1)

    def test_two_attachment_list(self):
        self.attachment_list = AttachmentList(self.example_attachment, self.example_attachment)
        self.assertEqual(len(self.attachment_list), 2)



class TestMessage(TestCommon):

    def test_message_mandatory_options(self):
        self.message = Message("#webops", "test message", "username")
        self.assertEqual(self.message['channel'], "#webops")
        self.assertEqual(self.message['text'], "test message")
        self.assertEqual(self.message['username'], "username")

    def test_message_attachment(self):
        self.message = Message("#webops", "test message", "username")
        self.message.attach("message", "hostname.domain", "CRITICAL")
        self.assertEqual(len(self.message['attachments']), 1)

    def test_message_multiple_attachment(self):
        self.message = Message("#webops", "test message", "username")
        self.message.attach("message", "hostname.domain", "CRITICAL")
        self.message.attach("message2", "hostname.domain", "CRITICAL")
        self.assertEqual(len(self.message['attachments']), 2)


if __name__ == '__main__':
    unittest.main()
