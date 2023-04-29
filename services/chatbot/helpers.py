from services.chatbot.models import ChatPrompt
from utils.lang_chain import LangChainConnector
from django_rq import job
from django.db import IntegrityError, transaction


class ChatHelper:

    def get_response(self, prompt: str) -> str:
        response = LangChainConnector().query(query=prompt)
        save_prompt_job.delay(prompt)
        return response

    @staticmethod
    def get_prompts():
        return list(ChatPrompt.objects.values_list("prompt", flat=True).order_by('-created_at'))


@job
@transaction.atomic
def save_prompt_job(prompt):
    try:
        prompt_instance = ChatPrompt(prompt=prompt)
        prompt_instance.save()
    except IntegrityError:
        # Prompt already exists, so don't save a duplicate
        pass
