# Helper functions for the rest of the app

def add_commas(number):
    return f"{number:,}"


def add_comas_decimals(number):
    return f"{number:,.2f}"


def avg_placement(json):
    total_placement_friends = 0
    for i in range(20):
        placement = json['matches'][i]['playerStats']['teamPlacement']
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