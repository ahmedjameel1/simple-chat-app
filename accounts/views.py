from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from chat.models import Message

# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        try:
            senders = []
            for message in Message.objects.filter(recipient=user):
                senders.append(message.sender.id)
            return redirect('chat', senders[0])
        except:
            return redirect('chat', 4)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'username does not exist!')

        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            senders = []
            for message in Message.objects.filter(recipient=user):
                senders.append(message.sender.id)
                return redirect('chat', senders[0])
        else:
            messages.error(request, 'username or password is incorrect!')

    return render(request, 'accounts/loginregister.html', {'page': page})


def logoutUser(request):
    logout(request)
    messages.success(request, 'user logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "user created!")
            return redirect('login')
    return render(request, 'accounts/loginregister.html', {'page': page, 'form': form})
