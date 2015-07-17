from django.test import TestCase, Client
from django.contrib.auth.models import User
from social_list.models import Player, Friendship, FriendshipRequest, Group, Membership
from social_list.factories import *
import urllib

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

class RegistrationTest(TestCase):

    def test_user_gets_redirected_on_home(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,settings.LOGIN_URL + "?next=/")

class SearchTest(TestCase):

    def test_user_can_search_for_users(self):
        user_1 = PlayerFactory()
        user_2 = PlayerFactory()
        user_3 = PlayerFactory()

        c = Client()
        params = urllib.parse.urlencode({
            "type":"User",
            "name":user_2.user.first_name
        })
        response = c.get("/search/?%s" % params)

        self.assertContains(response,user_2.user.first_name)
        self.assertNotContains(response,user_3.user.first_name)

    def test_user_can_search_group(self):
        group_1 = GroupFactory()
        group_2 = GroupFactory()
        group_2.name = "ANOTHER"
        group_2.save()

        c = Client()
        params = urllib.parse.urlencode({
            "type":"Group",
            "name":group_1.name
        })
        response = c.get("/search/?%s" % params)

        self.assertContains(response,group_1.name)
        self.assertNotContains(response,group_2.name)