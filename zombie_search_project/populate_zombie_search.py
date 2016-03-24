import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zombie_search_project.settings')

import django
django.setup()

from django.contrib.auth.hashers import make_password

from zombie_search.models import Player, Achievement, Badge, User

from datetime import date
import random

from game import Game
from streetfactory import StreetFactory
from game import PlayerState



#30 users
users = ["jill", "jim","joe","jen","bob","left4dead","zombie_game_king",
"youtube-gamer","@ttackOnTitan","C++","this.toString","TyreeseWilliams",
"SashaWilliams","ShaneWalsh","BobStookey","GabrielStokes","Bill","Francis",
"Louis", "Zoey", "Coach","Ellis", "Nick","Rochelle","ChrisRedfield",
"JillValentine","MarcusCampbell","EdJones","MayaTorres","MarcusGormley"]

badges = {"Killer":[0,"You have not earned the achievement yet.",
                    10,"You have killed 10 zombies.",
                    20,"You have killed 20 zombies.",
                    50,"You have killed 50 zombies."],
        "Survival":[0,"You have not earned the achievement yet.",
                    5,"You have surrived 5 days.",
                    10,"You have surrived 10 days.",
                    20,"You have surrived 20 days."],
        "Stamina":[0,"You have not earned the achievement yet.",
                    5,"You have played 5 games.",
                    10,"You have played 10 games.",
                    20,"You have played 20 games."],
        "Party":[0,"You have not earned the achievement yet.",
                    10,"You have had 10 people in your party.",
                    20,"You have had 20 people in your party.",
                    40,"You have had 40 people in your party."]}

def populate():
    print "Populating Badges..."
    for badge in badges:
        level = 0

        j=1 #For the description ie: "You have not earned the achievement yet."

        #i is for the criteria ie: 0
        for i in xrange(0,len(badges[badge]),2): #Iterate through each criteria for each level skiping description
            if level  == 3:
                icon = "\static\img\gold_cup.jpg"
            elif level  == 2:
                icon = "\static\img\silver_cup.jpg"
            elif level  == 1:
                icon = "\static\img" + r"\b"+ "ronze_cup.jpg" #python escape character
            else:
                icon = "\static\img"+ r"\n"+ "o_cup.jpg" #python escape character
            #For reference
            #add_badge(name,description,criteria,level,icon):
            add_badge(badge,badges[badge][j],badges[badge][i],level,icon)
            level = level +1
            j = j +2
    print("Done")

    print "Populating Users and Achievements..."
    #For reference
    #add_player(user, games_played, total_days, avg_days,most_days_survived, most_kills,total_kills,most_people):
    base_kills = 0
    base_days = 0
    days = 0
    threes = 0
    ones = 0
    twos = 0

    for name in users:

        user = add_user(name,make_password(name),True)

        games_played = twos
        total_days = base_days+threes
        most_days_survived = base_days+twos
        most_people = threes
        total_kills = base_kills+threes
        most_kills = base_kills +ones

        if threes != 0:
            avg_days = round((total_days/(twos*1.0)), 2)
        else:
            avg_days =0

        p = add_player(user, games_played, total_days, avg_days,
        most_days_survived, most_kills, total_kills, most_people)

        check_achievements(p)

        threes += 3
        ones += 1
        twos += 2
        base_kills = random.randint(0,10)
        base_days = random.randint(0,10)

        print("."),
    print("Done")


    print "...Zombie Search database population complete."

    # Print out Users and Players added to DB
    print "Users/Players"
    for u in User.objects.all():
        for p in Player.objects.filter(user=u):
            print "- {0}".format(str(p))
    print ""

    # Print out Badges added to DB
    print "Badges"
    for b in Badge.objects.all():
        print "- {0}".format(str(b))
    print ""

    # Print out Achievement added to DB
    print "Achievements"
    for a in Achievement.objects.all():
        print "- {0}".format(str(a))
    print ""



def check_achievements(player):

    for badge in Badge.objects.all():
        if badge.type == "Survival":
            if player.total_days >= badge.criteria:
                add_achievement(player,badge, date.today())
        if badge.type == "Killer":
            if player.total_days >= badge.criteria:
                add_achievement(player,badge, date.today())
        if badge.type == "Stamina":
            if player.games_played >= badge.criteria:
                add_achievement(player,badge, date.today())
        if badge.type == "Party":
            if player.most_people >= badge.criteria:
                add_achievement(player,badge, date.today())

    #add_achievement(player,b,date.today())


def add_badge(name,description,criteria,level,icon):
    b = Badge.objects.get_or_create(type = name,
    description = description,
    level=level,
    criteria = criteria,
    icon = icon)

    return b

def add_player(user, games_played, total_days, avg_days,
                most_days_survived, most_kills,total_kills,most_people):
    p = Player.objects.get_or_create(user=user)[0]
    g = Game()
    g.start_new_day()
    p.player_state=g.player_state
    p.update_state=g.update_state
    p.street=g.street
    p._time_left=g._time_left
    p.game_state=g.game_state
    p.games_played = games_played
    p.total_days = total_days
    p.avg_days = avg_days
    p.most_days_survived = most_days_survived
    p.most_kills = most_kills
    p.total_kills = total_kills
    p.most_people = most_people
    p.slug = user.username
    p.save()
    return p

def add_user(name,password,active):
    u = User.objects.get_or_create(username=name)[0]
    u.password = password
    u.email = name+"@glasgow.ac.uk"
    u.is_active = active
    u.save()
    return u

def add_achievement(player,badge,date):
    achievements = Achievement.objects.filter(player=player)
    try:
        for achievement in achievements:
            old_badge = achievement.badge
            if old_badge.type == badge.type:
                achievement.badge = badge #Change badge for this achievement to a level higer
                achievement.date_awarded=date #Change date
                achievement.save()
                return
    except:#If achievement does not exist, do nothing then create it
        pass
    a = Achievement.objects.get_or_create(player=player,
                                            badge=badge, date_awarded = date)


# Start execution here (^_^)V
if __name__ == '__main__':
    print "Starting Zombie Search database population script..."
    populate()
