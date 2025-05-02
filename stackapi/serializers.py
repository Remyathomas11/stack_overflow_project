from .models import AnswerVote, Question, Answer, Notification, QuestionVote
from rest_framework import serializers
from django.db.models import Count, Q


from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

class AnswerSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    class Meta:
        model = Answer
        fields = ['id','question', 'answer_text', 'user', 'created_at','upvotes', 'downvotes', 'is_accepted']
        read_only_fields = ['user', 'created_at']

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
