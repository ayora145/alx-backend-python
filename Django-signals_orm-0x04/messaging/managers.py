from django.db import models


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """Return only unread messages for a given user"""
        return self.filter(receiver=user, is_read=False).only("id", "content", "timestamp", "sender")