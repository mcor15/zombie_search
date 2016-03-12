#Vr.1 Matthew
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zombie_search_project.settings')

import django
django.setup()

from django.contrib.auth.hashers import make_password

from zombie_search.models import Player, Achievement, Badge, User

from datetime import date



users = ["jill", "jim","joe","Tyreese Williams","Sasha Williams","Shane Walsh",
"Bob Stookey","Gabriel Stokes","Bill","Francis", "Louis", "Zoey", "Coach",
 "Ellis", "Nick","Rochelle","Chris Redfield", "Jill Valentine",
  "Marcus Campbell","Ed Jones","Maya Torres","Marcus Gormley"]

badges = {"Za Killer not awarded":
            ["You are the killer of zombies.",
            [0]],
        "Za Killer Bronze":
            ["You are the killer of zombies.",
            [10]],
        "Za Killer Silver":
            ["You are the killer of zombies.",
            [20]],
        "Za Killer Gold":
            ["You are the killer of zombies.",
            [50]],
        "Zurvivalist not awarded":
            ["You've come this far but death does come to us all.",
            [0]],
        "Zurvivalist Bronze":
            ["You've come this far but death does come to us all.",
            [5]],
        "Zurvivalist Silver":
            ["You've come this far but death does come to us all.",
            [10]],
        "Zurvivalist Gold":
            ["You've come this far but death does come to us all.",
            [20]],
        "Stamina not awarded":
            ["You just can't get enough of this game.",
            [0]],
        "Stamina Bronze":
            ["You just can't get enough of this game.",
            [5]],
        "Stamina Silver":
            ["You just can't get enough of this game.",
            [10]],
        "Stamina Gold":
            ["You just can't get enough of this game.",
            [20]],
        "Party! not awarded":
            ["You just can't get enough of this game.",
            [0]],
        "Party! Bronze":
            ["You just can't get enough of this game.",
            [10]],
        "Party! Silver":
            ["You just can't get enough of this game.",
            [20]],
        "Party! Gold":
            ["You're everyone best friend...excpet zombies of course",
            [40]]}

def populate():
    print "Populating Badges..."
    for badge in badges:
        criteria = badges[badge][1][0]

        if badge[-4:] == "Gold":
            icon = "\static\img\gold_cup.jpg"
            level = 3
        elif badge[-6:] == "Silver":
            icon = "\static\img\silver_cup.jpg"
            level = 2
        elif badge[-6:] == "Bronze":
            icon = "\static\img" + r"\b"+ "ronze_cup.jpg" #python escape character
            level = 1
        else:
            icon = "\static\img"+ r"\n"+ "o_cup.jpg" #python escape character
            level = 0
        add_badge(badge,badges[badge][0],criteria,level,icon)
    print("Done")

    print "Populating Users and Achievements..."
    fives = 0
    twos = 0
    threes = 0
    for name in users:
        user = add_user(name,make_password(name),True)
        if threes != 0:
            avg_days = (twos/threes)
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
    for u in User.objects.all():
        for p in Player.objects.filter(user=u):
            print "- {0}".format(str(p))


def check_achievements(player):
    if player.games_played < 5:
        b = Badge.objects.get(type = "Stamina not awarded")
        #date(2016,06,16)
        add_achievement(player,b,date.today())
    if player.games_played >= 5:
        b = Badge.objects.get(type = "Stamina Bronze")
        #date(2016,06,16)
        add_achievement(player,b,date.today())
    if player.games_played >= 10:
        b = Badge.objects.get(type = "Stamina Silver")
        #date(2016,06,16)
        add_achievement(player,b,date.today())
    if player.games_played >= 20:
        b = Badge.objects.get(type = "Stamina Gold")
        #date(2016,06,16)
        add_achievement(player,b,date.today())

    if player.total_days < 10:
        b = Badge.objects.get(type = "Za Killer not awarded")
        #date(2016,06,16)
        add_achievement(player,b,date.today())
    if player.total_days >= 10:
        b = Badge.objects.get(type = "Za Killer Bronze")
        #date(2016,06,16)
        add_achievement(player,b,date.today())
    if player.total_days >= 20:
        b = Badge.objects.get(type = "Za Killer Silver")
        #date(2016,06,16)
        add_achievement(player,b,date.today())
    if player.total_days >= 50:
        b = Badge.objects.get(type = "Za Killer Gold")
        #date(2016,06,16)
        add_achievement(player,b,date.today())

    if player.most_people <10 :
        b = Badge.objects.get(type = "Party! not awarded")
        #date(2016,06,16)
        add_achievement(player,b,date.today())
    if player.most_people >= 10:
        b = Badge.objects.get(type = "Party! Bronze")
        #date(2016,06,16)
        add_achievement(player,b,date.today())
    if player.most_people >= 20:
        b = Badge.objects.get(type = "Party! Silver")
        #date(2016,06,16)
        add_achievement(player,b,date.today())
    if player.most_people >= 40:
        b = Badge.objects.get(type = "Party! Gold")
        #date(2016,06,16)
        add_achievement(player,b,date.today())


    if player.total_kills < 5:
        b = Badge.objects.get(type = "Zurvivalist not awarded")
        #date(2016,06,16)
        add_achievement(player,b,date.today())
    if player.total_kills >= 5:
        b = Badge.objects.get(type = "Zurvivalist Bronze")
        #date(2016,06,16)
        add_achievement(player,b,date.today())
    if player.total_kills >= 10:
        b = Badge.objects.get(type = "Zurvivalist Silver")
        #date(2016,06,16)
        add_achievement(player,b,date.today())
    if player.total_kills >= 20:
        b = Badge.objects.get(type = "Zurvivalist Gold")
        #date(2016,06,16)
        add_achievement(player,b,date.today())





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
    u.is_active = active
    u.save()
    return u

def add_achievement(player,badge,date):
    a = Achievement.objects.get_or_create(player=player,
                                            badge=badge, date_awarded = date)
    #a.save()


# Start execution here (^_^)V
if __name__ == '__main__':
    print "Starting Zombie Search database population script..."
    populate()
