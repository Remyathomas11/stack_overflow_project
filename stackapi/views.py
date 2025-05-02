from django.shortcuts import render

# Create your views here.


from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework import generics, permissions, filters
from .serializers import QuestionSerializer
from .models import Question, Answer, QuestionVote, AnswerVote 
from .serializers import AnswerSerializer, NotificationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from .models import Notification


class MyAPIView(APIView):
    def get(self, request):
        return Response({'message': 'GET'})

    def post(self, request):
        return Response({'message': 'POST'})

    def put(self, request):
        return Response({'message': 'PUT'})

    def patch(self, request):
        return Response({'message': 'PATCH'})

    def delete(self, request):
        return Response({'message': 'DELETE'})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return JsonResponse({'error': 'Please provide username, email, and password'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({'message': 'User created successfully'})

    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

# Create Question    
class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Update/Delete Question
class QuestionUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionDenied("Not your question.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
             raise PermissionDenied("Not your question.")
        instance.delete()

# List/Search Questions
class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Question.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'tags']  # Enables search by title or tag

#Answer  create
class AnswerCreateView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AnswerUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionDenied("Not your answer.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Not your answer.")
        instance.delete()

#Answer accept
class AcceptAnswerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, answer_id):
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return Response({"detail": "Answer not found."}, status=404)

        if answer.question.user != request.user:
            raise PermissionDenied("You can only accept answers to your own questions.")
            
        # Unmark previously accepted answers for the same question
        Answer.objects.filter(question=answer.question, is_accepted=True).update(is_accepted=False)

        answer.is_accepted = True
        answer.save()

         # Notify answer author
        if answer.user != request.user:
            Notification.objects.create(
                recipient=answer.user,
                message=f"Your answer to '{answer.question.title}' was accepted!"
            )

        return Response({"detail": "Answer marked as accepted."}, status=200)
       

   
#voting

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def vote_question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response({"detail": "Question not found."}, status=404)

    is_upvote = request.data.get("is_upvote", True)
    vote, created = QuestionVote.objects.update_or_create(
        user=request.user,
        question=question,
        defaults={"is_upvote": is_upvote}
    )

    upvotes = QuestionVote.objects.filter(question=question, is_upvote=True).count()
    downvotes = QuestionVote.objects.filter(question=question, is_upvote=False).count()

    return Response({
        "message": "Vote registered.",
        "upvotes": upvotes,
        "downvotes": downvotes
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def vote_answer(request, answer_id):
    try:
        answer = Answer.objects.get(pk=answer_id)
    except Answer.DoesNotExist:
        return Response({"detail": "Answer not found."}, status=404)

    is_upvote = request.data.get("is_upvote", True)
    vote, created = AnswerVote.objects.update_or_create(
        user=request.user,
        answer=answer,
        defaults={"is_upvote": is_upvote}
    )

    upvotes = AnswerVote.objects.filter(answer=answer, is_upvote=True).count()
    downvotes = AnswerVote.objects.filter(answer=answer, is_upvote=False).count()

    return Response({
        "message": "Vote registered.",
        "upvotes": upvotes,
        "downvotes": downvotes
    })
@api_view(['GET'])
def get_answers(request, question_id):
    answers = Answer.objects.filter(question_id=question_id)
    serializer = AnswerSerializer(answers, many=True)
    return Response(serializer.data)

# notification list view
class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')
