from django.db import models

# Create your models here.
from django.utils import timezone
import uuid



class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default="")
    player1_id = models.IntegerField(default=-1)
    player2_id = models.IntegerField(default=-1)
    game_state = models.CharField(max_length=50 ,default="in progress")
    player1_side = models.CharField(max_length=50,default="X")
    player2_side = models.CharField(max_length=50,default="O")
    tictactoe = models.CharField(max_length=9,default="---------")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    started_by = models.CharField(max_length=50,default="player1")
    current_player = models.IntegerField(default=-1)
    game_over = models.BooleanField(default=False)
    gameid = models.CharField(max_length=50,default="")

    def __str__(self):
        return self.name

class Gameuser(models.Model):
    name = models.CharField(max_length=50,default="")
    username = models.CharField(max_length=200, default="")
    password = models.CharField(max_length=200, default="")
    email = models.CharField(max_length=200, default="")
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    Games = models.ManyToManyField(Game)
    token = models.CharField(max_length=200, default=uuid.uuid4)


    def __str__(self):
        return self.username
