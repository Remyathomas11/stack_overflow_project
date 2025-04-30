# stackapi/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
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
]