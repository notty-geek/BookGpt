from services.chatbot.models import ChatPrompt
from utils.lang_chain import LangChainParser
from django_rq import job
from django.db import IntegrityError, transaction


class ChatHelper:

    def get_response(self, prompt: str) -> str:
        response = LangChainParser().query(query=prompt)
        save_prompt_job.delay(prompt)
        return response


@job
@transaction.atomic
def save_prompt_job(prompt):
    try:
        prompt_instance = ChatPrompt(prompt=prompt)
        prompt_instance.save()
    except IntegrityError:
        # Prompt already exists, so don't save a duplicate
        pass
