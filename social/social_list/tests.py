from django.test import TestCase
from django.contrib.auth.models import User
from social_list.models import Player, Friendship, FriendshipRequest, Group, Membership
import factory
import faker

faker = faker.Factory.create()

class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group
    name = "A new group"

class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.LazyAttribute(lambda o: faker.first_name())
    last_name = factory.LazyAttribute(lambda o: faker.last_name())
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())
    username = email

class PlayerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Player
    user = factory.SubFactory(UserFactory)

# Create your tests here.
class FriendshipTest(TestCase):

    def test_player_can_add_player(self):
        # Create two users
        user_1 = PlayerFactory()
        user_2 = PlayerFactory()

        # Call add function
        user_1.add_user(user_2)

        # Check if a FriendshipRequest was created
        friendship_request_list = FriendshipRequest.objects.all()
        self.assertEqual(len(friendship_request_list),1)

        # Check no Friendship were created
        friendship_list = Friendship.objects.all()
        self.assertEqual(len(friendship_list),0)

        # Check if users are correct
        friendship_request = friendship_request_list[0]
        self.assertEqual(friendship_request.user_from.user.first_name,user_1.user.first_name)
        self.assertEqual(friendship_request.user_to.user.first_name,user_2.user.first_name)

        # User 2 accepts the request from User 1
        user_2.accept_request_from_friend(user_1)

        # Check if FriendshipRequest is accepted
        friendship_request_list = FriendshipRequest.objects.all()
        friendship_request = friendship_request_list[0]
        self.assertEqual(friendship_request.accepted,True)

        # Check if both users have 1 friend each
        list_user1_friends = user_1.get_friend()

        self.assertEqual(len(list_user1_friends),1)
        self.assertEqual(list_user1_friends[0].user.first_name,user_2.user.first_name)

        list_user2_friends = user_2.get_friend()
        self.assertEqual(len(list_user1_friends),1)
        self.assertEqual(list_user2_friends[0].user.first_name,user_1.user.first_name)

    def test_user_can_only_accept_friend_requests_to_himself(self):
        user_1 = PlayerFactory()
        user_2 = PlayerFactory()
        user_3 = PlayerFactory()

        user_1.add_user(user_2)
        user_3.accept_request_from_friend(user_1)
        user_3.accept_request_from_friend(user_2)

        # Check if no FriendshipRequest is accepted
        friendship_request_list = FriendshipRequest.objects.all()
        friendship_request = friendship_request_list[0]
        self.assertEqual(friendship_request.accepted,False)
        

class GroupTest(TestCase):

    def test_user_can_join_group(self):
        user_1 = PlayerFactory()
        group_1 = GroupFactory()

        user_1.join_group(group_1)

        # Check if a Membership was created
        membership_list = Membership.objects.all()
        self.assertEqual(len(membership_list),1)

        # Check if Group member_list was updated
        self.assertEqual(len(group_1.member_list.all()),1)
