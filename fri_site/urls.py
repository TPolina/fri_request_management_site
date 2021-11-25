from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.index),
    path('hook/', views.show_request_on_page),
]
