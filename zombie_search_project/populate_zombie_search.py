#Vr.3 Matthew
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zombie_search_project.settings')

import django
django.setup()

from django.contrib.auth.hashers import make_password

from zombie_search.models import Player, Achievement, Badge, User

from datetime import date

from game import Game
from streetfactory import StreetFactory
from game import PlayerState

#28 users
users = ["jill", "jim","joe","left4dead","zombie_game_king","youtube-gamer","@ttackOnTitan",
"C++","this.toString","TyreeseWilliams","SashaWilliams","ShaneWalsh",
"BobStookey","GabrielStokes","Bill","Francis", "Louis", "Zoey", "Coach",
 "Ellis", "Nick","Rochelle","ChrisRedfield", "JillValentine",
  "MarcusCampbell","EdJones","MayaTorres","MarcusGormley"]

badges = {"Killer":{0:"You have not earned the achievement yet.",
                    10:"You have killed 10 zombies.",
                    20:"You have killed 20 zombies.",
                    50:"You have killed 50 zombies."},
        "Survival":{0:"You have not earned the achievement yet.",
                    5:"You have surrived 5 days.",
                    10:"You have surrived 10 days.",
                    20:"You have surrived 20 days."},
        "Stamina":{0:"You have not earned the achievement yet.",
                    5:"You have played 5 games.",
                    10:"You have played 10 games.",
                    20:"You have played 20 games."},
        "Party":{0:"You have not earned the achievement yet.",
                    10:"You have had 10 people in your party.",
                    20:"You have had 20 people in your party.",
                    40:"You have had 40 people in your party."}

def populate():
    print "Populating Badges..."
    for badge in badges:
        level = 0
        for criteria in badges[badge]:
            if level  == 3:
                icon = "\static\img\gold_cup.jpg"
            elif level  == 2:
                icon = "\static\img\silver_cup.jpg"
            elif level  == 1:
                icon = "\static\img" + r"\b"+ "ronze_cup.jpg" #python escape character
            else:
                icon = "\static\img"+ r"\n"+ "o_cup.jpg" #python escape character
            #print "badge>"+ badge+ " criteria>"+str(badges[badge][criteria])+" level>" +str(level) +" icon>" +icon
            add_badge(badge,badges[badge][criteria],criteria,level,icon)
            level = level +1
    print("Done")

    print "Populating Users and Achievements..."
    fives = 0
    twos = 0
    threes = 0
    for name in users:
        user = add_user(name,make_password(name),True)
        if threes != 0:
            avg_days = (twos/(threes*1.0))
        else:
            avg_days =0
        p = add_player(user, threes, twos, avg_days, threes, twos, fives, fives)
        check_achievements(p)
        fives = fives + 5
        twos = twos +2
        threes =threes +3
        print("."),
        #date = date(2016, 3, 11)
        #add_achievement(p,b, date(2016, 3, 11))
    print("Done")


    print "...Zombie Search database population complete."

    # Print out what we have added to the user.
    print "Users/Players"
    for u in User.objects.all():
        for p in Player.objects.filter(user=u):
            print "- {0}".format(str(p))
    print ""

    print "Badges"
    for b in Badge.objects.all():
        print "- {0}".format(str(b))
    print ""

    print "Achievements"
    for a in Achievement.objects.all():
        print "- {0}".format(str(a))
    print ""

    '''u= User.objects.all()
    u = u.get(username="Marcus Gormley")
    p = Player.objects.all()
    p = p.get(user=u)
    b = Badge.objects.all()
    b = b.get(type = "Killer")
    add_achievement(p,b, date(2026, 3, 11))'''

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
    #p.profile_picture =
    g = Game()
    g.start_new_day()
    p.player_state=g.player_state
    p.update_state=g.update_state
    p.street=g.street
    p.game_state=g.game_state
    p.games_played = games_played
    p.total_days = total_days
    p.avg_days = avg_days
    p.most_days_survived = most_days_survived
    p.most_kills = most_kills
    p.total_kills = total_kills
    p.most_people = most_people
    p.slug = user.username #make sure this works!!
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
    print player, badge, date
    achievements = Achievement.objects.filter(player=player)
    try:
        for achi in achievements:
            old_badge = achi.badge
            if old_badge.type == badge.type:
                achi.badge = badge
                achi.date_awarded=date
                achi.save()
                return
    except:
        pass
    a = Achievement.objects.get_or_create(player=player,
                                            badge=badge, date_awarded = date)
    #a.save()


# Start execution here (^_^)V
if __name__ == '__main__':
    print "Starting Zombie Search database population script..."
    populate()
