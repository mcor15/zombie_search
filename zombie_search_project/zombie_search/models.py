from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField

# Create your models here. \(^0^)/

class Player(models.Model):
    #One to one mapping of Player model to default User model
    user = models.OneToOneField(User)

    profile_picture = models.ImageField(blank=True)
    player_state = PickledObjectField()
    update_state = PickledObjectField()
    street = PickledObjectField()
    game_state = PickledObjectField()
    games_played = models.IntegerField(default=0)
    total_days = models.IntegerField(default=0)
    avg_days = models.FloatField(default=0.0)
    most_days_survived = models.IntegerField(default=0)
    most_kills = models.IntegerField(default=0)
    total_kills = models.IntegerField(default=0)
    most_people = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs): #Slug to be removed?
        self.slug = slugify(self.user.username)
        super(Player, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

class Badge(models.Model):
    type = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    criteria = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    icon = models.URLField(blank=True)#fixed???

    def __unicode__(self):
        return self.type

class Achievement(models.Model):
    player = models.ForeignKey(Player)
    badge = models.ForeignKey(Badge)
    date_awarded = models.DateField()

    def __unicode__(self):
        return self.badge.type
