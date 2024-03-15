import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from kingdomdeathapi.models import Player, Settlement
from rest_framework.authtoken.models import Token


class SettlementTests(APITestCase):

    fixtures = ['users', 'tokens', 'players', 'settlements']

    def setUp(self):
        # Try to retrieve the first existing Player object
        self.player = Player.objects.first()
        # Create a Token for the user if it doesn't exist
        token, created = Token.objects.get_or_create(user=self.player.user)
        # Set the client's credentials using the Token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        # Try to retrieve the first existing Settlement object
        self.settlement = Settlement.objects.first()

    def test_create_settlement(self):
        """
        Ensure we can create a new settlement.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/settlements"

        # Define the request body
        data = {
            "name": "Test",
            "survival_limit": 2,
            "population": 5,
            "game_master": self.player.id
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["name"], "Test")
        self.assertEqual(json_response["survival_limit"], 2)
        self.assertEqual(json_response["population"], 5)
        self.assertEqual(
            json_response["game_master"], {'id': 1, 'username': 'Twiknight'})

    def test_get_settlement(self):
        """
        Ensure we can get an existing settlement
        """

        # Initiate request and store response
        response = self.client.get(f"/settlements/{self.settlement.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the settlement was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["name"], "Yharnam")
        self.assertEqual(json_response["survival_limit"], 4)
        self.assertEqual(json_response["population"], 3)
        self.assertEqual(
            json_response["game_master"], {'id': 1, 'username': 'Twiknight'})

    def test_change_settlement(self):
        """
        Ensure we can change an existing settlement.
        """

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "name": "New",
            "survival_limit": 4,
            "population": 10,
            "game_master": {'id': 1, 'username': 'Twiknight'}
        }

        response = self.client.put(
            f"/settlements/{self.settlement.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET settlement again to verify changes were made
        response = self.client.get(f"/settlements/{self.settlement.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "New")
        self.assertEqual(json_response["survival_limit"], 4)
        self.assertEqual(json_response["population"], 10)
        self.assertEqual(json_response["game_master"], {'id': 1, 'username': 'Twiknight'})

    def test_delete_settlement(self):
        """
        Ensure we can delete an existing settlement.
        """

        # DELETE the settlement you just created
        response = self.client.delete(f"/settlements/{self.settlement.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the settlement again to verify you get a 404 response
        response = self.client.get(f"/settlements/{self.settlement.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
