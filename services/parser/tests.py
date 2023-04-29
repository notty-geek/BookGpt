from django.test import TestCase

# Create your tests here.
import os
from unittest import TestCase, mock
from utils.lang_chain import LangChainConnector

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

from services.pdfparser.task import parse_pdf_task


class ParsePDFViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_parse_pdf_view(self):
        # Construct a mock request object with data containing PDF URLs.
        data = {'urls': ['http://example.com/pdf1', 'http://example.com/pdf2']}
        response = self.client.post('/v1/parse-pdf/', data)

        # Assert that the response status code is 202.
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # Assert that the response body contains a 'message' key with a non-empty value.
        self.assertIn('message', response.data)
        self.assertNotEqual(response.data['message'], '')

    def test_invalid_parse_pdf_view(self):
        # Construct a mock request object with invalid data.
        data = {'invalid_field': 'http://example.com/pdf'}
        response = self.client.post('/v1/parser/pdf/', data)

        # Assert that the response status code is 400.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_pdf_urls(self):
        # Construct a mock request object with an empty list of PDF URLs.
        data = {'urls': []}
        response = self.client.post('/v1/parser/pdf/', data)

        # Assert that the response status code is 400.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the response body contains a 'urls' key with an error message.
        self.assertIn('urls', response.data)
        self.assertEqual(response.data['urls'][0], 'This list may not be empty.')

    @patch('services.pdfparser.views.enqueue')
    def test_parse_pdf_task_enqueueing(self, mock_enqueue):
        # Construct a mock request object with data containing PDF URLs.
        data = {'urls': ['http://example.com/pdf']}
        response = self.client.post('/v1/parser/pdf/', data)

        # Assert that the response status code is 202.
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # Assert that the parse_pdf_task function was called with the PDF URLs list.
        mock_enqueue.assert_called_once_with(parse_pdf_task, ['http://example.com/pdf'])

    @patch('services.pdfparser.views.enqueue', side_effect=Exception('test error'))
    def test_parse_pdf_view_error(self, mock_enqueue):
        # Construct a mock request object with data containing PDF URLs.
        data = {'urls': ['http://example.com/pdf']}
        response = self.client.post('/v1/parser/pdf/', data)

        # Assert that the response status code is 500.
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Assert that the response body contains an 'error' key with a non-empty value.
        self.assertIn('error', response.data)
        self.assertNotEqual(response.data['error'], '')


class TestLangChainConnector(TestCase):

    def setUp(self):
        self.pdf_urls = ['http://example.com/document.pdf']
        self.mock_loader = mock.Mock()
        self.mock_loader.load.return_value = ['Document text']
        self.mock_embeddings = mock.Mock()
        self.mock_docs = ['Document text']
        self.mock_text_splitter = mock.Mock()
        self.mock_text_splitter.split_documents.return_value = self.mock_docs
        self.mock_docsearch = mock.Mock()
        self.mock_docsearch.similarity_search.return_value = self.mock_docs
        self.mock_llm = mock.Mock()
        self.mock_chain = mock.Mock()
        self.mock_chain.run.return_value = 'Answer'

    @mock.patch('utils.lang_chain.Pinecone')
    @mock.patch('utils.lang_chain.OnlinePDFLoader')
    @mock.patch('utils.lang_chain.OpenAIEmbeddings')
    @mock.patch('utils.lang_chain.CharacterTextSplitter')
    def test_ingest_pdf(self, mock_text_splitter, mock_embeddings, mock_loader, mock_pinecone):
        # Set up the test
        connector = LangChainConnector()
        mock_text_splitter.return_value = self.mock_text_splitter
        mock_embeddings.return_value = self.mock_embeddings
        mock_loader.return_value = self.mock_loader
        mock_pinecone.from_documents.return_value = None

        # Call the method being tested
        connector.ingest_pdf(self.pdf_urls)

        # Assert that the expected methods are called with the correct arguments
        mock_loader.assert_called_once_with(self.pdf_urls[0])
        mock_loader.return_value.load.assert_called_once_with()
        mock_text_splitter.assert_called_once_with(chunk_size=1000, chunk_overlap=0)
        mock_text_splitter.return_value.split_documents.assert_called_once_with(self.mock_docs)
        mock_embeddings.assert_called_once_with(openai_api_key=os.getenv("OPENAI_API_KEY", ))
        mock_pinecone.from_documents.assert_called_once_with(self.mock_docs, self.mock_embeddings,
                                                             index_name=os.getenv("PINECONE_INDEX"))
