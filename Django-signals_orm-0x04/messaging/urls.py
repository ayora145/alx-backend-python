from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_messages, name='conversation'),
    path('delete-user/', views.delete_user, name='delete_user'),
]