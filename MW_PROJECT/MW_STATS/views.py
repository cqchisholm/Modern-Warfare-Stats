from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests
from .helpers import *
from .forms import LoginForm, RegisterForm, FriendsForm
from .models import Friends, Score, User, Profile
from time import sleep


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

    # get the API response for warzone stats for the user
    url_user = "https://call-of-duty-modern-warfare.p.rapidapi.com/warzone/{}/xbl".format(gamertag)
    headers = {
    'x-rapidapi-key': "206fdfeafcmsh70f2e07b4f4d6e0p136146jsn19dcf2a2f09e",
    'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com"
    }
    # Response for user
    response_user = requests.request('GET', url_user, headers=headers)
    wz_stats = response_user.json()

    # all warzone stats
    kd = '{:.2f}'.format(round(wz_stats['br']['kdRatio'], 3))
    downs = add_commas(wz_stats['br']['downs'])
    downs_per_game = '{:.2f}'.format(round(wz_stats['br']['downs'] / wz_stats['br']['gamesPlayed'], 2))
    kills = add_commas(wz_stats['br']['kills'])
    kills_per_game = '{:.2f}'.format(round(wz_stats['br']['kills'] / wz_stats['br']['gamesPlayed'], 2))
    deaths = add_commas(wz_stats['br']['deaths'])
    games_played = add_commas(wz_stats['br']['gamesPlayed'])
    wins = add_commas(wz_stats['br']['wins'])
    win_percentage = '{:.2f}'.format(round(wz_stats['br']['wins'] / wz_stats['br']['gamesPlayed'] * 100, 2))
    top5_percentage = '{:.2f}'.format(round(wz_stats['br']['topFive'] / wz_stats['br']['gamesPlayed'] * 100, 2))
    top5 = add_commas(wz_stats['br']['topFive'])
    top10 = add_commas(wz_stats['br']['topTen'])
    top25 = add_commas(wz_stats['br']['topTwentyFive'])
    revives = add_commas(wz_stats['br']['revives'])
    sleep(1)

    #############################################################################
    # All same info above but for all friends added for that user to compare with
    friends = Friends.objects.filter(user=request.user).first()
    friends_list = [friends.gamertag1, friends.gamertag2, friends.gamertag3, friends.gamertag4, friends.gamertag5]
    # get the API response for warzone stats for the friends of the user
    wz_stats_F = []
    for friend in friends_list:
        stats_list =[]
        # if there is a gamertag than get the stats, otherwise continue
        if friend != '':
            url_friends = "https://call-of-duty-modern-warfare.p.rapidapi.com/warzone/{}/xbl".format(friend)
            headers = {
            'x-rapidapi-key': "206fdfeafcmsh70f2e07b4f4d6e0p136146jsn19dcf2a2f09e",
            'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com"
            }

            # response for the friends - already have headers from above
            response_friends = requests.request('GET', url_friends, headers=headers)
            wz_stats_friends = response_friends.json()

            # all warzone stats for friends
            kd_f = '{:.2f}'.format(round(wz_stats_friends['br']['kdRatio'], 3))
            downs_f = add_commas(wz_stats_friends['br']['downs'])
            downs_per_game_f = '{:.2f}'.format(round(wz_stats_friends['br']['downs'] / wz_stats_friends['br']['gamesPlayed'], 2))
            kills_f = add_commas(wz_stats_friends['br']['kills'])
            kills_per_game_f = '{:.2f}'.format(round(wz_stats_friends['br']['kills'] / wz_stats_friends['br']['gamesPlayed'], 2))
            deaths_f = add_commas(wz_stats_friends['br']['deaths'])
            games_played_f = add_commas(wz_stats_friends['br']['gamesPlayed'])
            wins_f = add_commas(wz_stats_friends['br']['wins'])
            win_percentage_f = '{:.2f}'.format(round(wz_stats_friends['br']['wins'] / wz_stats_friends['br']['gamesPlayed'] * 100, 2))
            top5_percentage_f = '{:.2f}'.format(round(wz_stats_friends['br']['topFive'] / wz_stats_friends['br']['gamesPlayed'] * 100, 2))
            top5_f = add_commas(wz_stats_friends['br']['topFive'])
            top10_f = add_commas(wz_stats_friends['br']['topTen'])
            revives_f = add_commas(wz_stats_friends['br']['revives'])

            # gather into a list
            stats_list.extend([
                friend, win_percentage_f, top5_percentage_f, 
                wins_f, top5_f, top10_f, kills_f,
                deaths_f, kd_f, downs_f, downs_per_game_f, kills_per_game_f, revives_f, games_played_f
                ]
            )
            wz_stats_F.append(stats_list)
            sleep(1) # Sleep for 1 second to avoid API calls/sec error
        else:
            continue

    return render(request, 'mw_stats/warzone.html', {
        'gamertag': gamertag,
        'kd': kd,
        'downs': downs,
        'downs_per_game': downs_per_game,
        'kills_per_game': kills_per_game,
        'wins': wins,
        'kills': kills,
        'deaths': deaths,
        'games_played': games_played,
        'win_percentage': win_percentage,
        'top5_percentage': top5_percentage,
        'top5': top5,
        'top10': top10,
        'top25': top25,
        'revives': revives,
        'wz_stats_F': wz_stats_F
    })


@login_required
def multiplayer(request):
    # get the gamertag of the signed in user via the Profile
    profile = Profile.objects.filter(user=request.user).first()
    gamertag = profile.gamertag

    # get the API response for warzone stats for the user
    url_user = "https://call-of-duty-modern-warfare.p.rapidapi.com/multiplayer/{}/xbl".format(gamertag)
    headers = {
    'x-rapidapi-key': "206fdfeafcmsh70f2e07b4f4d6e0p136146jsn19dcf2a2f09e",
    'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com"
    }
    # Response for user
    response_user = requests.request('GET', url_user, headers=headers)
    mp_stats = response_user.json()

    # all warzone stats
    kills = add_commas(mp_stats['lifetime']['all']['properties']['kills'])
    killstreak = mp_stats['lifetime']['all']['properties']['recordKillStreak']
    deaths = add_commas(mp_stats['lifetime']['all']['properties']['deaths'])
    kd = round(mp_stats['lifetime']['all']['properties']['kdRatio'], 3)
    best_kd = round(mp_stats['lifetime']['all']['properties']['bestKD'], 3)
    assists = add_commas(mp_stats['lifetime']['all']['properties']['assists'])
    score_per_game = add_commas(round(mp_stats['lifetime']['all']['properties']['scorePerGame'], 2))
    score_per_min = add_commas(round(mp_stats['lifetime']['all']['properties']['scorePerMinute'], 2))
    wins = add_commas(mp_stats['lifetime']['all']['properties']['wins'])
    win_perc = round(mp_stats['lifetime']['all']['properties']['winLossRatio'], 3) * 100
    sleep(1)

    #############################################################################
    # All same info above but for all friends added for that user to compare with
    friends = Friends.objects.filter(user=request.user).first()
    friends_list = [friends.gamertag1, friends.gamertag2, friends.gamertag3, friends.gamertag4, friends.gamertag5]
    # get the API response for warzone stats for the friends of the user
    mp_stats_F = []
    for friend in friends_list:
        stats_list =[]
        # if there is a gamertag than get the stats, otherwise continue
        if friend != '':
            url_friends = "https://call-of-duty-modern-warfare.p.rapidapi.com/multiplayer/{}/xbl".format(friend)
            headers = {
            'x-rapidapi-key': "206fdfeafcmsh70f2e07b4f4d6e0p136146jsn19dcf2a2f09e",
            'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com"
            }

            # response for the friends - already have headers from above
            response_friends = requests.request('GET', url_friends, headers=headers)
            mp_stats_friends = response_friends.json()

            # all warzone stats for friends
            kills_f = add_commas(mp_stats_friends['lifetime']['all']['properties']['kills'])
            killstreak_f = mp_stats_friends['lifetime']['all']['properties']['recordKillStreak']
            deaths_f = add_commas(mp_stats_friends['lifetime']['all']['properties']['deaths'])
            kd_f = round(mp_stats_friends['lifetime']['all']['properties']['kdRatio'], 3)
            best_kd_f = round(mp_stats_friends['lifetime']['all']['properties']['bestKD'], 3)
            assists_f = add_commas(mp_stats_friends['lifetime']['all']['properties']['assists'])
            score_per_game_f = add_commas(round(mp_stats_friends['lifetime']['all']['properties']['scorePerGame'], 2))
            score_per_min_f = add_commas(round(mp_stats_friends['lifetime']['all']['properties']['scorePerMinute'], 2))
            wins_f = add_commas(mp_stats_friends['lifetime']['all']['properties']['wins'])
            win_perc_f = round(mp_stats_friends['lifetime']['all']['properties']['winLossRatio'], 3) * 100

            # gather into a list
            stats_list.extend([
                friend, kills_f, killstreak_f, deaths_f,
                kd_f, best_kd_f, assists_f, score_per_game_f,
                score_per_min_f, wins_f, win_perc_f
                ]
            )
            mp_stats_F.append(stats_list)
            sleep(1) # Sleep for 1 second to avoid API calls/sec error
        else:
            continue
    return render(request, 'mw_stats/multiplayer.html', {
        'gamertag': gamertag,
        'kills': kills,
        'killstreak': killstreak,
        'deaths': deaths,
        'kd': kd,
        'best_kd': best_kd,
        'assists': assists,
        'score_per_game': score_per_game,
        'score_per_min': score_per_min,
        'wins': wins,
        'win_perc': win_perc,
        'mp_stats_F': mp_stats_F
    })


@login_required
def friends(request):
    if request.method == 'POST':
        form = FriendsForm(request.POST)
        if form.is_valid():
            Friends.objects.update_or_create(
                user=request.user,
                defaults={
                    'gamertag1': form.cleaned_data['gamertag1'],
                    'gamertag2': form.cleaned_data['gamertag2'],
                    'gamertag3': form.cleaned_data['gamertag3'],
                    'gamertag4': form.cleaned_data['gamertag4'],
                    'gamertag5': form.cleaned_data['gamertag5']
                }
            )
            return HttpResponseRedirect(reverse('warzone'))
        else:
            return render(request, 'mw_stats/friends.html', {
                'form': FriendsForm(),
                'message': 'DID NOT WORK FOR SOME REASON'
            })

    # if method == GET
    return render(request, 'mw_stats/friends.html', {
        'form': FriendsForm()
    })


@login_required
def history(request):
    # get the gamertag of the signed in user via the Profile
    profile = Profile.objects.filter(user=request.user).first()
    gamertag = profile.gamertag

    # get hgistory stats from API
    url_user = "https://call-of-duty-modern-warfare.p.rapidapi.com/warzone-matches/{}/xbl".format(gamertag)
    headers = {
        'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com",
        'x-rapidapi-key': "206fdfeafcmsh70f2e07b4f4d6e0p136146jsn19dcf2a2f09e"
        }
    response = requests.request('GET', url_user, headers=headers)
    history_stats = response.json()

    # special cases needed
    kd = round(history_stats['summary']['all']['kdRatio'], 3)

    sleep(1) # sleep to avoid API calls/sec error

    # using functions in 'helpers' - finding the avergae palcement, best finish, most kills over the last 20 games
    avg_placement_user = avg_placement(history_stats)
    best_placement_user = best_placement(history_stats)
    most_kills_user = most_kills(history_stats)

    #############################################################################
    # get list of friends of the user
    friends = Friends.objects.filter(user=request.user).first()
    friends_list = [friends.gamertag1, friends.gamertag2, friends.gamertag3, friends.gamertag4, friends.gamertag5]

    # get history stats for all friends
    wz_stats_friends = []
    for friend in friends_list:
        stats_list_friends = []
        if friend != '':
            url_friend = "https://call-of-duty-modern-warfare.p.rapidapi.com/warzone-matches/{}/xbl".format(friend)
            response_friends = requests.request('GET', url_friend, headers=headers)
            history_stats_friends = response_friends.json()

            avg_placement_friend = avg_placement(history_stats_friends)
            best_placement_friend = best_placement(history_stats_friends)
            most_kills_friend = most_kills(history_stats_friends)
            kd_friend = round(history_stats_friends['summary']['all']['kdRatio'], 3)

            stats_list_friends.extend([friend, avg_placement_friend, best_placement_friend, most_kills_friend, history_stats_friends, kd_friend])
            wz_stats_friends.append(stats_list_friends)
        else:
            continue
        
    return render(request, 'mw_stats/history.html', {
        'gamertag': gamertag,
        'history_stats': history_stats,
        'friends_list': friends_list,
        'avg_placement_user': avg_placement_user,
        'best_placement_user': best_placement_user,
        'most_kills_user': most_kills_user,
        'kd': kd,
        'wz_stats_friends': wz_stats_friends
    })


@login_required
def private(request):
    alex_scores = Score.objects.filter(id=1).first()
    colin_scores = Score.objects.filter(id=2).first()
    trace_scores = Score.objects.filter(id=3).first()


    if request.method == 'POST':
        first = request.POST['first']
        second = request.POST['second']
        third = request.POST['third']
        
        


        return render(request, 'mw_stats/private.html')

    else:
        return render(request, 'mw_stats/private.html', {
            'alex_scores': alex_scores,
            'colin_scores': colin_scores,
            'trace_scores': trace_scores
        })