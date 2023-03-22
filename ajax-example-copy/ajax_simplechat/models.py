from django.db import models
from django.contrib.auth.models import User


class AjaxItem(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)

    def __str__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + '"'
