from unittest import TestCase

from BE.src.preprocessing.emojis_parser import emojis_to_description


class TestEmoji2Description(TestCase):

    def test_single_emoji(self):
        text = '😀'
        expected_output = 'grinsendes gesicht'
        self.assertEqual(expected_output, emojis_to_description(text))

    def test_multiple_emojis(self):
        text = '😀 😆😂'
        expected_output = 'grinsendes gesicht grinsegesicht mit zugekniffenen augengesicht mit freudentränen'
        self.assertEqual(expected_output, emojis_to_description(text))

    def test_text_with_emoji(self):
        text = 'Hallo 😀 Welt!'
        expected_output = 'Hallo grinsendes gesicht Welt!'
        self.assertEqual(expected_output, emojis_to_description(text))
