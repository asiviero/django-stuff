from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User)
    friend_list = models.ManyToManyField('self',through='Friendship',
                                                                        through_fields=('user_from','user_to'),
                                                                        symmetrical=False)

# Create your models here.
class Friendship(models.Model):
    user_from = models.ForeignKey(Player)
    user_to = models.ForeignKey(Player,related_name="friend")
