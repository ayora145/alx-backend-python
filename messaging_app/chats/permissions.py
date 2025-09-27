# messaging_app/chats/permissions.py
from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from .models import Conversation

class IsParticipantOfConversation(BasePermission):
    """
    Permission that allows access only to participants of a conversation.
    - has_permission: ensures request.user is authenticated and for POST creates checks conversation from payload
    - has_object_permission: checks membership for Conversation or Message objects
    """

    def has_permission(self, request, view):
        # deny anonymous requests
        if not request.user or not request.user.is_authenticated:
            return False

        # If creating (POST) a Message, ensure the user is a participant of the provided conversation id
        is_create = request.method == "POST" and getattr(view, "action", None) in (None, "create")
        if is_create:
            conv_id = None
            if isinstance(request.data, dict):
                conv_id = request.data.get("conversation") or request.data.get("conversation_id")
            if conv_id:
                try:
                    conv = Conversation.objects.get(pk=conv_id)
                except ObjectDoesNotExist:
                    return False
                return request.user in conv.participants.all()
        return True

    def has_object_permission(self, request, view, obj):
        # If the object has participants (Conversation model)
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # If object is a Message with a conversation field
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        # default deny
        return False
