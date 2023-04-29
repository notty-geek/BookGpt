from rest_framework.views import APIView
from rest_framework.response import Response
from services.chatbot.serializers import ChatRequestSerializer
from services.chatbot.helpers import ChatHelper
import logging


class ChatHandlerView(APIView):
    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sanitized_prompt = serializer.validated_data['prompt'].strip().replace('\n', ' ')
        try:
            response = ChatHelper().get_response(sanitized_prompt)
            return Response(response, status=200)

        except Exception as e:
            error_message = 'Something went wrong'
            logging.error(f'Error in ChatHandlerView: {e}')
            return Response({'error': error_message}, status=500)



class ChatPromptView(APIView):

    def get(self, request):
        try:
            prompts = ChatHelper.get_prompts()
            return Response(prompts, status=200)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=500)
