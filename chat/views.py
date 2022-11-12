from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from itertools import chain
from .utils import search

# Create your views here.
@login_required(login_url="login")
def chat(request,pk):
    if request.method == 'POST':
       body = request.POST['body']
       message = Message.objects.create(body=body,sender=request.user,recipient=User.objects.get(id=pk))
       message.save() 
       return redirect('chat', User.objects.get(id=pk).id)
    else:
        user = request.user  
        recipient = User.objects.get(id=pk)
        senders = []
        for message in Message.objects.filter(recipient=user):
            senders.append(message.sender.id)
        for message in Message.objects.filter(sender=user):
            senders.append(message.recipient.id)
        messagers = User.objects.filter(id__in=senders)
        recieved_messages = Message.objects.filter(sender=recipient,recipient=user).order_by('created')
        sent_messages = Message.objects.filter(sender=user,recipient=recipient).order_by('created')
        messages = recieved_messages | sent_messages
        nmessages = messages.order_by('created')
        for message in recieved_messages:
            message.is_read == True
            message.save()
    users, search_query = search(request)
    return render(request, 'chat/chat.html', {'user':user, 'messagers':messagers,
    'recipient':recipient, 'nmessages':nmessages,'users':users,})


