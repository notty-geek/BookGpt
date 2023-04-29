from django.db import models


class ChatPrompt(models.Model):
    prompt = models.TextField(unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Prompt {self.pk}, {self.prompt}'
