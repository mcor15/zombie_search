from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=10)
    email = models.CharField(max_length=20)
	
    profile_picture = models.ImageField(blank=True)
	
    games_played = models.IntegerField(default=0)
    total_days = models.IntegerField(default=0)
	#How do we calculate this within the database?
    avg_days = models.IntegerField(default=0)
    most_days_survived = models.IntegerField(default=0)
    most_kills = models.IntegerField(default=0)
    total_kills = models.IntegerField(default=0)
    most_people = models.IntegerField(default=0)
	

    def __unicode__(self):
        return self.name


class Badge(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=20)
    criteria = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    icon = models.ImageField()

    def __unicode__(self):
        return self.name


class Achievement(models.Model):
    player = models.ForeignKey(Player)
    badge = models.ForeignKey(Badge)
    date_awarded = models.DateField()

    def __unicode__(self):
        return self.name
