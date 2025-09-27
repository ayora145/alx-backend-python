# chats/permissions.py
from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - Only authenticated users can access
    - Only participants in a conversation can send/view/update/delete messages
    """

    def has_object_permission(self, request, view, obj):
        # Check if the request user is part of the conversation
        return request.user in obj.participants.all()
