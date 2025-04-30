from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    voters = models.ManyToManyField(User, related_name='voted_questions', through='QuestionVote')

    def __str__(self):
        return self.title  
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    voters = models.ManyToManyField(User, related_name='voted_answers', through='AnswerVote')

    def __str__(self):
        return f'Answer by {self.user.username} to {self.question.title}'
    
class QuestionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()  # True = upvote, False = downvote

    class Meta:
        unique_together = ('user', 'question')  # user can vote once

class AnswerVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

    class Meta:
        unique_together = ('user', 'answer')

