from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from services.parser.serializer import PDFURLSerializer
from django_rq import enqueue
from services.parser.task import parse_pdf_task
import logging



class ParsePDFView(APIView):

    def post(self, request):
        try:
            serializer = PDFURLSerializer(data=request.data)
            if serializer.is_valid():
                pdf_urls = serializer.validated_data.get('urls', [])
                queue_task = [enqueue(parse_pdf_task, urls) for urls in pdf_urls]
                return Response({'message': f'{len(queue_task)} PDF parsing jobs queued'},
                                status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = 'Something went wrong'
            logging.error(f'Error in ChatHandlerView: {e}')
            return Response({'error': error_message}, status=500)
