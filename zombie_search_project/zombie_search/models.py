from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here. \(^0^)/

class Player(models.Model):
    #One to one mapping of Player model to default User model
    user = models.OneToOneField(User)
	
    profile_picture = models.ImageField(upload_to='player_avatars', blank=True)
    games_played = models.IntegerField(default=0)
    total_days = models.IntegerField(default=0)
	#How do we calculate this within the database?
    avg_days = models.IntegerField(default=0)
    most_days_survived = models.IntegerField(default=0)
    most_kills = models.IntegerField(default=0)
    total_kills = models.IntegerField(default=0)
    most_people = models.IntegerField(default=0)
	

    def __unicode__(self):
        return self.user.username


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
