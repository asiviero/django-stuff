from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User)
    friend_list = models.ManyToManyField('self',through='Friendship',
                                                                        through_fields=('user_from','user_to'),
                                                                        symmetrical=False)
    friend_request_list = models.ManyToManyField('self',through='FriendshipRequest',
                                                                        through_fields=('user_to','user_from'),
                                                                        symmetrical=False,
                                                                        related_name = 'request_list')
    def add_user(self,friend,message=""):
        FriendshipRequest.objects.create(
            user_from = self,
            user_to = friend,
            message = message,
        )

    def get_friend(self,friend_id=None):
        return self.friend_list.all()

    def accept_request_from_friend(self,friend):
        FriendshipRequest.objects.get(user_from=friend).accept()

class Friendship(models.Model):
    user_from = models.ForeignKey(Player)
    user_to = models.ForeignKey(Player,related_name="friend")

class FriendshipRequest(models.Model):
    user_from = models.ForeignKey(Player,related_name="friend_ask")
    user_to = models.ForeignKey(Player,related_name="friend_asked")
    message = models.TextField(default="Hi, I wanna be your friend")
    accepted = models.BooleanField(default = False)
    def accept(self):
        # Creates two Friendship
        Friendship.objects.create(
            user_from = self.user_from,
            user_to = self.user_to
        )

        Friendship.objects.create(
            user_from = self.user_to,
            user_to = self.user_from
        )
        self.accepted = True
        self.save()
