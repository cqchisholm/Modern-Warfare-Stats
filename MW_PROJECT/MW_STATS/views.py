from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests
from .helpers import *
from .forms import LoginForm, RegisterForm, FriendsForm
from .models import User, Profile


def index(request):
    # if user is signed in
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        gamertag = profile.gamertag
        return render(request, 'mw_stats/index.html', {
            'gamertag': gamertag
        })
    # if no user is signed in
    else:
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


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'mw_stats/login.html', {
                    'form': LoginForm(),
                    'message': 'User does not exist.'
                })
        else:
            return render(request, 'mw_stats/login.html', {
                'form': LoginForm(),
                'message': 'The form was not filled out correctly. CHANGE THIS MESSAGE.'
            })
    else:
        return render(request, 'mw_stats/login.html', {
            'form': LoginForm()
        })


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def warzone(request):
    # get the gamertag of the signed in user via the Profile
    profile = Profile.objects.filter(user=request.user).first()
    gamertag = profile.gamertag

    # get the API response for warzone stats
    url = "https://call-of-duty-modern-warfare.p.rapidapi.com/warzone/{}/xbl".format(gamertag)
    headers = {
    'x-rapidapi-key': "206fdfeafcmsh70f2e07b4f4d6e0p136146jsn19dcf2a2f09e",
    'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com"
    }
    response = requests.request('GET', url, headers=headers)
    wz_stats = response.json()

    # all warzone stats
    kd = round(wz_stats['br']['kdRatio'], 3)
    downs = add_commas(wz_stats['br']['downs'])
    top25 = add_commas(wz_stats['br']['topTwentyFive'])
    kills = add_commas(wz_stats['br']['kills'])
    deaths = add_commas(wz_stats['br']['deaths'])
    games_played = add_commas(wz_stats['br']['gamesPlayed'])
    wins = add_commas(wz_stats['br']['wins'])
    win_percentage = round(wz_stats['br']['wins'] / wz_stats['br']['gamesPlayed'] * 100, 2)
    top5_percentage = round(wz_stats['br']['topFive'] / wz_stats['br']['gamesPlayed'] * 100, 2)
    top5 = add_commas(wz_stats['br']['topFive'])
    top10 = add_commas(wz_stats['br']['topTen'])
    top25 = add_commas(wz_stats['br']['topTwentyFive'])
    revives = add_commas(wz_stats['br']['revives'])

    return render(request, 'mw_stats/warzone.html', {
        'gamertag': gamertag,
        'kd': kd,
        'downs': downs,
        'wins': wins,
        'top25': top25,
        'kills': kills,
        'deaths': deaths,
        'games_played': games_played,
        'win_percentage': win_percentage,
        'top5_percentage': top5_percentage,
        'top5': top5,
        'top10': top10,
        'top25': top25,
        'revives': revives
    })


@login_required
def friends(request):
    if request.method == 'POST':
        # REMOVE THE BELOW. THIS IS JUST FOR TEST.
        return HttpResponseRedirect(reverse('index'))
    # if method == GET
    return render(request, 'mw_stats/friends.html', {
        'form': FriendsForm()
    })