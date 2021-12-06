from django.urls import path
from . import views

app_name = 'fri_site'
urlpatterns = [
    path('', views.index, name='index'),
    path('hook/', views.add_user_and_message_from_bot, name='hook'),
    path('<int:update_id>/', views.edit_message, name='edit_message'),
]
