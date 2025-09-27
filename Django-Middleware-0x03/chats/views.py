from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message

@login_required
def chat_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(user=request.user, content=content)
            return JsonResponse({'status': 'success'})
    
    messages = Message.objects.all().order_by('-timestamp')[:50]
    return render(request, 'chats/chat.html', {'messages': messages})

def home_view(request):
    return render(request, 'chats/home.html')