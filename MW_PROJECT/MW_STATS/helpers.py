from .models import PrivateUsers

# Helper functions for the rest of the app

def add_commas(number):
    return f"{number:,}"


def add_comas_decimals(number):
    return f"{number:,.2f}"


def avg_placement(json):
    total_placement_friends = 0
    for i in range(20):
        placement = json['matches'][i]['playerStats']['teamPlacement']
        print(placement)
        total_placement_friends += placement
    placement = round(total_placement_friends / 20)
    return placement


def best_placement(json):
    best = 300
    for i in range(20):
        placement = json['matches'][i]['playerStats']['teamPlacement']
        if placement < best:
            best = placement
    return best


def most_kills(json):
    most = 0
    for i in range(20):
        kills = json['matches'][i]['playerStats']['kills']
        if kills > most:
            most = kills
    return most


def sorted_friends_list():
    alex_private = PrivateUsers.objects.get(id=1)
    colin_private = PrivateUsers.objects.get(id=2)
    trace_private = PrivateUsers.objects.get(id=3)
    player_list = [
        ('Alex', alex_private.all_time_score),
        ('Colin', colin_private.all_time_score),
        ('Trace', trace_private.all_time_score)
    ]
    sorted_list = sorted(player_list, key=lambda x: x[1], reverse=True)
    return sorted_list
