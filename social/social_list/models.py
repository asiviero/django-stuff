from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

class Player(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=255, default="")
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
        try:
            FriendshipRequest.objects.get(user_from=friend,user_to=self).accept()
        except FriendshipRequest.DoesNotExist:
            pass

    def join_group(self,group):
        Membership.objects.create(
            member = self,
            group = group
        )

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['nickname']

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.user_name = self.cleaned_data["first_name"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

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

class Group(models.Model):
    name = models.CharField(max_length = 255)
    member_list = models.ManyToManyField(Player,through='Membership')

class Membership(models.Model):
    member = models.ForeignKey(Player)
    group = models.ForeignKey(Group)
