from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import MessageFilter



class ConversationViewSet(viewsets.ModelViewSet):
    """
    Conversations viewset - only participants can see a conversation
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]  # also require auth via settings
     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ["created_at", "sender"]
    ordering = ["-created_at"]  # newest first

    def perform_create(self, serializer):
        conversation = serializer.save()
        # Add participants from request data
        participant_ids = self.request.data.get('participant_ids', [])
        conversation.participants.set(participant_ids)
     def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)
  

class MessageViewSet(viewsets.ModelViewSet):
    """
    Messages viewset - only participants can list/create/read/update/delete messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(conversation__participants=user).order_by('-created_at')

    def perform_create(self, serializer):
        # ensure sender is request.user if your serializer has a sender field
        serializer.save(sender=self.request.user)

    


    

