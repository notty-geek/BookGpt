import logging
from urllib.parse import urlparse
from rest_framework import serializers
from django.core.exceptions import ValidationError
import requests


class PDFURLSerializer(serializers.Serializer):
    urls = serializers.ListField(child=serializers.URLField())

    def check_pdf_url(self, url):
        response = requests.head(url)
        if response.status_code == requests.codes.ok:
            content_type = response.headers.get('content-type')
            if content_type and 'application/pdf' in content_type.lower():
                return True
        return False

    def validate_urls(self, value):
        if not value:
            raise ValidationError('At least one URL is required.')
        unique_urls = set()
        for url in value:
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValidationError('Invalid URL: {}'.format(url))
            if parsed_url.path[-4:].lower() != '.pdf':
                raise ValidationError('Only PDF files are accepted.')
            if url in unique_urls:
                raise ValidationError('Duplicate URL: {}'.format(url))
            unique_urls.add(url)
            if not self.check_pdf_url(url):
                raise ValidationError('PDF file not found at URL: {}, Please enter valid Pdf List and try'.format(url))
        return value
