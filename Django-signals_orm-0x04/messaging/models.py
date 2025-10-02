from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# ✅ Custom Manager
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        # Return only unread messages for a given user
        return self.filter(user=user, read=False).only("id", "content", "created_at")
        # `.only()` makes query faster by fetching only necessary fields


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}: {self.content[:20]}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - Message {self.message.id}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of {self.message.id} at {self.edited_at}"


# ✅ New field for threaded replies
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

      # ✅ New field for read/unread
    read = models.BooleanField(default=False)

    # Attach the custom manager
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager


    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"

    # ✅ Recursive function to fetch threaded replies
    def get_all_replies(self):
        replies = []
        for reply in self.replies.all().select_related('user').prefetch_related('replies'):
            replies.append(reply)
            replies.extend(reply.get_all_replies())  # recursion
        return replies