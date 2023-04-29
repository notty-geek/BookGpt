from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from unittest.mock import patch

import os
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ChatHandlerViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_chat_handler_view(self):
        # Construct a mock request object with data containing a prompt.
        data = {'prompt': 'Hello, how are you?'}
        response = self.client.post('/v1/chat/', data)


        # Assert that the response status code is 200.
        self.assertEqual(response.status_code, 200)

        # Assert that the response body contains a 'response' key with a non-empty value.
        self.assertIn('response', response.data)
        self.assertNotEqual(response.data['response'], '')

    def test_invalid_chat_handler_view(self):
        # Construct a mock request object with invalid data.
        data = {'invalid_field': 'Hello, how are you?'}
        response = self.client.post('/v1/chat/', data)

        # Assert that the response status code is 400.
        self.assertEqual(response.status_code, 400)

    def test_chat_prompt_view(self):
        response = self.client.get('/v1/prompts/')

        # Assert that the response status code is 200.
        self.assertEqual(response.status_code, 200)

        # Assert that the response body is a list of prompts.
        self.assertIsInstance(response.data, list)


@override_settings(LOGGING_CONFIG=None)
class ChatHandlerViewErrorTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('services.chatbot.helpers.ChatHelper.get_response', side_effect=Exception('test error'))
    def test_chat_handler_view_error(self, mock_get_response):
        # Construct a mock request object with data containing a prompt.
        data = {'prompt': 'Hello, how are you?'}
        response = self.client.post('/v1/chat/', data)

        # Assert that the response status code is 500.
        self.assertEqual(response.status_code, 500)

        # Assert that the response body contains an 'error' key with a non-empty value.
        self.assertIn('error', response.data)
        self.assertNotEqual(response.data['error'], '')
