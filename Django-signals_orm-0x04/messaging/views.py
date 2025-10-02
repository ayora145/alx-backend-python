from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message


@login_required
def delete_user(request):
    user = request.user
    user.delete()  # This triggers post_delete signal
    return redirect('home')  # redirect to homepage or goodbye page

@cache_page(60)  # cache for 60 seconds
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id)
    return render(request, 'chats/conversation_messages.html', {'messages': messages})


