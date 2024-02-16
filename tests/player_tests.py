import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from kingdomdeathapi.models import Player
from rest_framework.authtoken.models import Token


class PlayerTests(APITestCase):

    fixtures = ['users', 'tokens', 'players',]

    def setUp(self):
        # Try to retrieve the first existing Player object
        self.player = Player.objects.first()
        # Create a Token for the user if it doesn't exist
        token, created = Token.objects.get_or_create(user=self.player.user)
        # Set the client's credentials using the Token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_player(self):
        """
        Ensure we can get an existing player
        """

        # Initiate request and store response
        response = self.client.get(f"/players/{self.player.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the player was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["is_game_master"], True)

    def test_change_player(self):
        """
        Ensure we can change an existing player.
        """

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "first_name": "Daniel",
            "last_name": "Myers",
            "username": "danielmyers",
            "email": "daniel@myers.com",
            "is_game_master": False
        }

        response = self.client.put(
            f"/players/{self.player.id}", data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET player again to verify changes were made
        response = self.client.get(f"/players/{self.player.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["first_name"], "Daniel")
        self.assertEqual(json_response["last_name"], "Myers")
        self.assertEqual(json_response["username"], "danielmyers")
        self.assertEqual(json_response["email"], "daniel@myers.com")
        self.assertEqual(json_response["is_game_master"], False)

    def test_delete_player(self):
        """
        Ensure we can delete an existing player.
        """
        
        # Seed the database with a user (use a unique username)
        user = User.objects.create(username="gatoradephilips", password="password", first_name="Gatorade", last_name="Philips",
                                   email="gatorade@philips.com", is_staff=False, is_active=True, date_joined="2022-10-21T21:19:24.892Z")

        # Seed the database with a player
        player = Player.objects.create(
            user=user, is_game_master=True)

        # DELETE the player you just created
        response = self.client.delete(f"/players/{player.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the player again to verify you get a 404 response
        response = self.client.get(f"/players/{player.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
