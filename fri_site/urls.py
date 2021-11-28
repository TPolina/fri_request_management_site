from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.index),
    path('hook/', views.add_request_from_bot),
]
