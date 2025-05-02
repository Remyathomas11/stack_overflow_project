from .models import AnswerVote, Question, Answer, Notification, QuestionVote
from rest_framework import serializers
from django.db.models import Count, Q

class AnswerSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    class Meta:
        model = Answer
        fields = ['id','question', 'answer_text', 'user', 'created_at','upvotes', 'downvotes']
       

    def get_upvotes(self, obj):
        return AnswerVote.objects.filter(answer=obj, is_upvote=True).count()

    def get_downvotes(self, obj):
        return AnswerVote.objects.filter(answer=obj, is_upvote=False).count()

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'tags', 'user', 'answers']
        read_only_fields = ['user', 'created_at']
    def get_upvotes(self, obj):
        return QuestionVote.objects.filter(answer=obj, is_upvote=True).count()

    def get_downvotes(self, obj):
        return QuestionVote.objects.filter(answer=obj, is_upvote=False).count()

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'created_at', 'is_read']
