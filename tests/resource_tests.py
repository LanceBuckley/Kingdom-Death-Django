import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from kingdomdeathapi.models import Player, Resource
from rest_framework.authtoken.models import Token


class ResourceTests(APITestCase):

    fixtures = ['users', 'tokens', 'players', 'resources', 'resource_types']

    def setUp(self):
        # Try to retrieve the first existing Player object
        self.player = Player.objects.first()
        # Create a Token for the user if it doesn't exist
        token, created = Token.objects.get_or_create(user=self.player.user)
        # Set the client's credentials using the Token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        # Try to retrieve the first existing Resource object
        self.resource = Resource.objects.first()

    def test_create_resource(self):
        """
        Ensure we can create a new resource.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/resources"

        # Define the request body
        data = {
            "name": "Test",
            "type": 2
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["name"], "Test")
        self.assertEqual(json_response["type"], {'id': 2, 'name': 'Bone'})

    def test_get_resource(self):
        """
        Ensure we can get an existing resource
        """

        # Initiate request and store response
        response = self.client.get(f"/resources/{self.resource.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the resource was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["name"], "Hide")
        self.assertEqual(json_response["type"], {'id': 1, 'name': 'Hide'})

    def test_change_resource(self):
        """
        Ensure we can change an existing resource.
        """

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "name": "New",
            "type": 4
        }

        response = self.client.put(
            f"/resources/{self.resource.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET resource again to verify changes were made
        response = self.client.get(f"/resources/{self.resource.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "New")
        self.assertEqual(json_response["type"], {'id': 4, 'name': 'Scrap'})

    def test_delete_resource(self):
        """
        Ensure we can delete an existing resource.
        """

        # DELETE the resource you just created
        response = self.client.delete(f"/resources/{self.resource.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the resource again to verify you get a 404 response
        response = self.client.get(f"/resources/{self.resource.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
