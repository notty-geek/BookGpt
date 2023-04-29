from django.core.exceptions import ValidationError
from rest_framework import serializers


class PDFURLSerializer(serializers.Serializer):
    urls = serializers.ListField(child=serializers.URLField())

    def validate_urls(self, value):
        if not value:
            raise ValidationError('At least one URL is required.')
        for url in value:
            if not url.endswith('.pdf'):
                raise ValidationError('Only PDF files are accepted.')
        return list(set(value))
