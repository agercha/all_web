from django.db import models
from django.contrib.auth.models import User

class PFP(models.Model):
  pfp_user      = models.CharField(max_length=100, default="")
  picture       = models.FileField(blank=True)
  content_type  = models.CharField(max_length=50)

  def __str__(self):
      return 'id=' + str(self.id) + ', user=' + self.pfp_user

class Post(models.Model):
  content       = models.CharField(max_length=1000)
  author        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
  date_time     = models.DateTimeField()

  def __str__(self):
    return f"{self.author}: {self.content} ({self.date_time})"

class Comment(models.Model):
  content       = models.CharField(max_length=1000)
  author        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
  date_time     = models.DateTimeField()
  post          = models.IntegerField()
  
  def __str__(self):
    return f"{self.author}: {self.content} ({self.date_time})"

class Profile(models.Model):
  user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
  first_name  = models.CharField(max_length=20)
  last_name   = models.CharField(max_length=20)
  bio         = models.CharField(max_length=200)
  profile_pic = models.FileField(blank=True, null=True)
  pfp_type    = models.CharField(max_length=100, blank=True, null=True)
  friends     = models.ManyToManyField(User)

  def __str__(self):
      return f"{self.first_name} {self.last_name}"