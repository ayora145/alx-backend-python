
# messaging_app/chats/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .Views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
