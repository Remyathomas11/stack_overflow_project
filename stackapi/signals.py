# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Answer, Notification

@receiver(post_save, sender=Answer)
def notify_question_owner_on_new_answer(sender, instance, created, **kwargs):
    if created:
        question = instance.question
        if question.user != instance.user:  # Avoid notifying self-answer
            Notification.objects.create(
                recipient=question.user,
                message=f"New answer posted to your question: '{question.title}'"
            )
