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


def main():



    print("as")
    print("as")
    print("as")
