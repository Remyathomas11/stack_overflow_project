# stackapi/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .views import (
    MyAPIView,RegisterView, QuestionCreateView, QuestionUpdateDeleteView, QuestionListView, AnswerUpdateDeleteView, AnswerCreateView, AcceptAnswerView, NotificationListView
)



urlpatterns = [
    path('api/my-endpoint/', MyAPIView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('questions/', QuestionCreateView.as_view(), name='create_question'),
    path('questions/update-delete/<int:pk>/', QuestionUpdateDeleteView.as_view(), name='question-update-delete'),
    path('answers/', AnswerCreateView.as_view(), name='post-answer'),
    path('questions/list/', QuestionListView.as_view(), name='questions-list'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('questions/<int:question_id>/vote/', views.vote_question, name='vote-question'),
    path('answers/<int:answer_id>/vote/', views.vote_answer, name='vote-answer'),
    path('answers/update-delete/<int:pk>/', AnswerUpdateDeleteView.as_view(), name='answer-update-delete'),
    path('answers/<int:answer_id>/accept/', AcceptAnswerView.as_view(), name='accept-answer'),
    path('notifications/', NotificationListView.as_view(), name='notifications')



]