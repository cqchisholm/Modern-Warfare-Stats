from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from .models import User, Profile


def index(request):
    return render(request, 'mw_stats/index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            gamertag = form.cleaned_data['gamertag']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            profile = Profile(user=user, gamertag=gamertag)
            profile.save()
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                return render(request, 'mw_stats/index.html', {
                    'form': RegisterForm(),
                    'message': 'Unable to authenticate the user.'
                })
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'mw_stats/index.html', {
                'form': RegisterForm(),
                'message': 'The form was not filled out correctly. CHANGE THIS MESSAGE.'
            })
    else:
        return render(request, 'mw_stats/register.html', {
            'form': RegisterForm()
        })