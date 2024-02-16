import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from kingdomdeathapi.models import Player, SettlementInventory
from rest_framework.authtoken.models import Token


class SettlementInventoryTests(APITestCase):

    fixtures = ['users', 'tokens', 'players', 'settlements', 'settlement_inventories', 'resources', 'resource_types']

    def setUp(self):
        # Try to retrieve the first existing Player object
        self.player = Player.objects.first()
        # Create a Token for the user if it doesn't exist
        token, created = Token.objects.get_or_create(user=self.player.user)
        # Set the client's credentials using the Token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        # Try to retrieve the first existing Settlement object
        self.settlement_inventory = SettlementInventory.objects.first()

    def test_create_settlement_inventory(self):
        """
        Ensure we can create a new settlement_inventory.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/settlement_inventories"

        # Define the request body
        data = {
            "settlement": 1,
            "resource": 2,
            "amount": 5,
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["settlement"], 1)
        self.assertEqual(json_response["resource"], {'id': 2, 'name': "Bone", 'type': {'id': 2, 'name': "Bone"}})
        self.assertEqual(json_response["amount"], 5)

    def test_get_settlement_inventory(self):
        """
        Ensure we can get an existing settlement_inventory
        """

        # Initiate request and store response
        response = self.client.get(f"/settlement_inventories/{self.settlement_inventory.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the settlement_inventory was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["settlement"], 7)
        self.assertEqual(json_response["resource"], {'id': 1, 'name': "Hide", 'type': {'id': 1, 'name': "Hide"}})
        self.assertEqual(json_response["amount"], 2)

    def test_change_settlement_inventory(self):
        """
        Ensure we can change an existing settlement_inventory.
        """

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "settlement": 1,
            "resource": 2,
            "amount": 2,
        }

        response = self.client.put(
            f"/settlement_inventories/{self.settlement_inventory.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET settlement_inventory again to verify changes were made
        response = self.client.get(f"/settlement_inventories/{self.settlement_inventory.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["settlement"], 1)
        self.assertEqual(json_response["resource"], {'id': 2, 'name': "Bone", 'type': {'id': 2, 'name': "Bone"}})
        self.assertEqual(json_response["amount"], 2)

    def test_delete_settlement_inventory(self):
        """
        Ensure we can delete an existing settlement_inventory.
        """

        # DELETE the settlement_inventory you just created
        response = self.client.delete(f"/settlement_inventories/{self.settlement_inventory.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the settlement_inventory again to verify you get a 404 response
        response = self.client.get(f"/settlement_inventories/{self.settlement_inventory.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
