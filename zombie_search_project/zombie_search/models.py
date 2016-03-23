from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField
from game import Game
from datetime import date

# Create your models here. \(^0^)/

class Player(models.Model):
    #One to one mapping of Player model to default User model
    user = models.OneToOneField(User)

    profile_picture = models.ImageField(upload_to = "player-proflies", blank=True)
    player_state = PickledObjectField()
    update_state = PickledObjectField()
    street = PickledObjectField()
    game_state = PickledObjectField()
    _time_left=PickledObjectField(default=100)
    games_played = models.IntegerField(default=0)
    total_days = models.IntegerField(default=0)
    avg_days = models.FloatField(default=0.0)
    most_days_survived = models.IntegerField(default=0)
    most_kills = models.IntegerField(default=0)
    total_kills = models.IntegerField(default=0)
    most_people = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Player, self).save(*args, **kwargs)

    def update_game(self,player_state,street,update_state,game_state,_time_left):
        self.player_state=player_state
        self.update_state=update_state
        self.game_state=game_state
        self._time_left=_time_left
        self.street=street
        self.save()

    def game_over_update(self, days, kills, party):
        self.total_days+=days
        self.games_played+=1
        self.total_kills+=kills
        self.avg_days=float(self.total_days)/float(self.games_played)
        if self.most_days_survived < days:
            self.most_days_survived = days
        if self.most_kills < kills:
            self.most_kills = kills
        if self.most_people < party:
            self.most_people = party
        check_achievements(self)
        self.save()


    def __unicode__(self):
        return self.user.username

class Badge(models.Model):
    type = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    criteria = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    icon = models.URLField(blank=True)

    def __unicode__(self):
        return self.type

class Achievement(models.Model):
    player = models.ForeignKey(Player)
    badge = models.ForeignKey(Badge)
    date_awarded = models.DateField()

    def __unicode__(self):
        return self.badge.type

def check_achievements(player):
    for badge in Badge.objects.all():
        if badge.type == "Survival":
            if player.total_days >= badge.criteria:
                add_achievement(player,badge, date.today())
        if badge.type == "Killer":
            if player.most_kills >= badge.criteria:
                add_achievement(player,badge, date.today())
        if badge.type == "Stamina":
            if player.games_played >= badge.criteria:
                add_achievement(player,badge, date.today())
        if badge.type == "Party":
            if player.most_people >= badge.criteria:
                add_achievement(player,badge, date.today())

def add_achievement(player,badge,date):
        achievements = Achievement.objects.filter(player=player)
        for achi in achievements:
            old_badge = achi.badge
            if old_badge.type == badge.type:
                achi.badge = badge
                achi.date_awarded=date
                achi.save()
                return

