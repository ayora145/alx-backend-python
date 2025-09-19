from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        # Add participants from request data
        participant_ids = self.request.data.get('participant_ids', [])
        conversation.participants.set(participant_ids)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
