# views.py
from django.shortcuts import render, redirect
from .models import AI, Message

def ai_profile(request, ai_id):
    ai = AI.objects.get(id=ai_id)
    return render(request, 'ai_models/ai_profile.html', {'ai': ai})

def post_message(request, ai_id):
    ai = AI.objects.get(id=ai_id)
    if request.method == 'POST':
        message = request.POST['message']
        ai.messages.create(content=message)
        return redirect('ai_profile', ai_id=ai.id)
    return render(request, 'ai_models/post_message.html', {'ai': ai})

def follow_ai(request, ai_id):
    ai = AI.objects.get(id=ai_id)
    user = request.user
    user.following.add(ai)
    return redirect('ai_profile', ai_id=ai.id)

def ai_feed(request):
    ais = AI.objects.all()
    messages = []
    for ai in ais:
        messages.extend(ai.messages.all())
    return render(request, 'ai_models/ai_feed.html', {'messages': messages})