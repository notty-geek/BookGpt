from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from services.parser.serializer import PDFURLSerializer
from django.core.exceptions import ValidationError


class ParsePDFViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('parser:pdf')
        print(self.url)

    def test_parse_pdf_view_with_valid_urls(self):
        """
        Test if ParsePDFView returns HTTP 202 status code and correct message when valid PDF URLs are provided.
        """
        pdf_urls = [
            "https://www.learnandmaster.com/resources/Learn-and-Master-Guitar-Lesson-Book.pdf"
        ]
        data = {'urls': pdf_urls}
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data, {'message': f'{len(pdf_urls)} PDF parsing jobs queued'})

    def test_parse_pdf_view_with_invalid_urls(self):
        """
        Test if ParsePDFView returns HTTP 400 status code and correct error message when invalid PDF URLs are provided.
        """
        pdf_urls = [
            'https://example.com/example1.pdf',
            'https://example.com/example2.html',
        ]
        data = {'urls': pdf_urls}
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        serializer = PDFURLSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(response.data, serializer.errors)

    def test_parse_pdf_view_with_empty_urls(self):
        """
        Test if ParsePDFView returns HTTP 400 status code and correct error message when no PDF URLs are provided.
        """
        data = {'urls': []}
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        serializer = PDFURLSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(response.data, serializer.errors)

    def test_parse_pdf_view_with_duplicate_urls(self):
        """
        Test if ParsePDFView returns HTTP 400 status code and correct error message when duplicate PDF URLs are provided.
        """
        pdf_urls = [
            'https://example.com/example1.pdf',
            'https://example.com/example2.pdf',
            'https://example.com/example1.pdf',
        ]
        data = {'urls': pdf_urls}
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        serializer = PDFURLSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(response.data, serializer.errors)

    def test_parse_pdf_view_with_invalid_url_format(self):
        """
        Test if ParsePDFView returns HTTP 400 status code and correct error message when invalid PDF URL format is provided.
        """
        pdf_urls = [
            'https://example.com/example1.pdf',
            'example.com/example2.pdf',
        ]
        data = {'urls': pdf_urls}
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        serializer = PDFURLSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(response.data, serializer.errors)

    def test_parse_pdf_view_with_unreachable_urls(self):
        """
        Test if ParsePDFView returns HTTP 400 status code and correct error message when PDF URLs are unreachable.
        """
        pdf_urls = [
            'https://example.com/example1.pdf'
        ]
        data = {'urls': pdf_urls}
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
