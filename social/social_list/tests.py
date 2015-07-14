from django.test import TestCase
from django.contrib.auth.models import User
from social_list.models import Player
import factory
import faker

faker = faker.Factory.create()

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

        # Check if both users have 1 friend each
        list_user1_friends = user_1.get_friend()

        self.assertEqual(len(list_user1_friends),1)
        self.assertEqual(list_user1_friends[0].user.first_name,user_2.user.first_name)

        list_user2_friends = user_2.get_friend()
        self.assertEqual(len(list_user1_friends),1)
        self.assertEqual(list_user2_friends[0].user.first_name,user_1.user.first_name)
