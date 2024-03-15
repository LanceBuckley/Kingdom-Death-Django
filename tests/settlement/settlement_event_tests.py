import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from kingdomdeathapi.models import Player, SettlementEvent
from rest_framework.authtoken.models import Token


class SettlementEventTests(APITestCase):

    fixtures = ['users', 'tokens', 'players', 'settlements', 'settlement_events', 'events']

    def setUp(self):
        # Try to retrieve the first existing Player object
        self.player = Player.objects.first()
        # Create a Token for the user if it doesn't exist
        token, created = Token.objects.get_or_create(user=self.player.user)
        # Set the client's credentials using the Token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        # Try to retrieve the first existing Settlement object
        self.settlement_event = SettlementEvent.objects.first()

    def test_create_settlement_event(self):
        """
        Ensure we can create a new settlement_event.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/settlement_events"

        # Define the request body
        data = {
            "settlement": 1,
            "event": 2,
            "year": 5,
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created event are correct
        self.assertEqual(json_response["settlement"], 1)
        self.assertEqual(json_response["event"], {'id': 2, 'name': "Clinging Mist"})
        self.assertEqual(json_response["year"], 5)

    def test_get_settlement_event(self):
        """
        Ensure we can get an existing settlement_event
        """

        # Initiate request and store response
        response = self.client.get(f"/settlement_events/{self.settlement_event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the settlement_event was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["settlement"], 2)
        self.assertEqual(json_response["event"], {'id': 1, 'name': "Acid Storm"})
        self.assertEqual(json_response["year"], 1)

    def test_change_settlement_event(self):
        """
        Ensure we can change an existing settlement_event.
        """

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "settlement": 1,
            "event": {'id': 1, 'name': "Acid Storm"},
            "year": 3,
        }

        response = self.client.put(
            f"/settlement_events/{self.settlement_event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET settlement_event again to verify changes were made
        response = self.client.get(f"/settlement_events/{self.settlement_event.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["settlement"], 1)
        self.assertEqual(json_response["event"], {'id': 1, 'name': "Acid Storm"})
        self.assertEqual(json_response["year"], 3)

    def test_delete_settlement_event(self):
        """
        Ensure we can delete an existing settlement_event.
        """

        # DELETE the settlement_event you just created
        response = self.client.delete(f"/settlement_events/{self.settlement_event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the settlement_event again to verify you get a 404 response
        response = self.client.get(f"/settlement_events/{self.settlement_event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
