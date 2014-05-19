import unittest

from icinga_slack.webhook import AttachmentField, AttachmentFieldList, Attachment, AttachmentList, Message

class TestCommon(unittest.TestCase):

    def setUp(self):
        self.example_attachment_field = {"title": "My Title", "value": "My Value"}
        self.example_attachment_field2 = {"title": "My Second Title", "value": "My Second Value", "short": True}
        self.example_attachment_field_list = [self.example_attachment_field]
        self.example_attachment_field_list2 = [self.example_attachment_field, self.example_attachment_field2]

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
        attachment = Attachment("Fallback Message", self.example_attachment_field_list)

    def test_attachment_with_optionals(self):
        attachment = Attachment("Fallback Message", self.example_attachment_field_list, "Text", "Pretext", "#FF0000")


if __name__ == '__main__':
    unittest.main()
