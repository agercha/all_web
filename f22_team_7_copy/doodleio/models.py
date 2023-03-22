from django.db import models

from django.contrib.auth.models import User

class PlayerItem(models.Model):
   isDrawing = models.BooleanField(default=False)
   hasDrawn = models.BooleanField(default=False)
   inGameRoom = models.BooleanField(default=False)
   inLeaderBoardRoom = models.BooleanField(default=False)
   guessedRight = models.BooleanField(default=False)
   startTime = models.IntegerField(default=60)
   word = models.CharField(max_length=20)
   score = models.IntegerField()
   name = models.CharField(max_length=20)
 
   def __str__(self):
       return 'id=' + str(self.id) + ',name="' + self.name + '"'
   
   @staticmethod
   def get_players_status():
       return PlayerItem.objects.all()
   
   @staticmethod
   def get_players_drawing_status():
       for player in PlayerItem.objects.all():
           print(player.name)
           print("Player.hasDrawn:", player.hasDrawn)
           print("Player.isDrawing:", player.isDrawing)
   
   

# Create your models here.
class ChatItem(models.Model):
   text = models.CharField(max_length=200)
   user = models.CharField(max_length=20)
   color = models.CharField(max_length=20)
  #  user = models.ForeignKey(User, default=None,            
  #   on_delete=models.PROTECT)
   correct_guess = models.BooleanField()
 
   def __str__(self):
       return 'id=' + str(self.id) + ',text="' + self.text + '", user=' + self.user 

class RoundItem(models.Model):
    players = models.ManyToManyField(PlayerItem)
    word = models.CharField(max_length=20)
    # timer = models.IntegerField(default=60)
    startTime = models.IntegerField(default=60)