# stackapi/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .views import QuestionCreateView
from .views import AnswerCreateView
from .views import QuestionListView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('questions/', QuestionCreateView.as_view(), name='create_question'),
    path('answers/', AnswerCreateView.as_view(), name='post-answer'),
    path('questionslist/', QuestionListView.as_view(), name='questions-list'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('questions/<int:question_id>/vote/', views.vote_question, name='vote-question'),
    path('answers/<int:answer_id>/vote/', views.vote_answer, name='vote-answer'),


]