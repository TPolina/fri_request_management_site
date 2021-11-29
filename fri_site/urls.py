from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('hook/', views.add_user_and_message_from_bot),
]
