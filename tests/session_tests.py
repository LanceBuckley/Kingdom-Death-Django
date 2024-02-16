import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from kingdomdeathapi.models import Player, Session
from rest_framework.authtoken.models import Token


class SessionTests(APITestCase):

    fixtures = ['users', 'tokens', 'players', 'settlements', 'sessions']

    def setUp(self):
        # Try to retrieve the first existing Player object
        self.player = Player.objects.first()
        # Create a Token for the user if it doesn't exist
        token, created = Token.objects.get_or_create(user=self.player.user)
        # Set the client's credentials using the Token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        # Try to retrieve the first existing Session object
        self.session = Session.objects.first()

    def test_create_session(self):
        """
        Ensure we can create a new session.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/sessions"

        # Define the request body
        data = {
            "host": 1,
            "settlement": 1,
            "players": [1, 2, 4]
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created session are correct
        self.assertEqual(
            json_response["host"], {'id': 1, 'username': 'Twiknight'})
        self.assertEqual(
            json_response["settlement"], 1)
        self.assertEqual(
            json_response["players"], [
                {'id': 1, 'username': 'Twiknight'},
                {'id': 2, 'username': 'RockZak'},
                {'id': 4, 'username': 'JJDuyne'}
                ])

    def test_get_session(self):
        """
        Ensure we can get an existing session
        """

        # Initiate request and store response
        response = self.client.get(f"/sessions/{self.session.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the session was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(
            json_response["host"], {'id': 1, 'username': 'Twiknight'})
        self.assertEqual(
            json_response["settlement"], 1)
        self.assertEqual(
            json_response["players"], [
                {'id': 1, 'username': 'Twiknight'},
                {'id': 2, 'username': 'RockZak'},
                {'id': 3, 'username': 'Bob1'}
                ])

    def test_change_session(self):
        """
        Ensure we can change an existing session.
        """

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "host": 1,
            "settlement": 1,
            "players": [1, 3, 4, 5]
        }

        response = self.client.put(
            f"/sessions/{self.session.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET session again to verify changes were made
        response = self.client.get(f"/sessions/{self.session.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json_response["host"], {'id': 1, 'username': 'Twiknight'})
        self.assertEqual(
            json_response["settlement"], 1)
        self.assertEqual(
            json_response["players"], [
                {'id': 1, 'username': 'Twiknight'},
                {'id': 3, 'username': 'Bob1'},
                {'id': 4, 'username': 'JJDuyne'},
                {'id': 5, 'username': 'Erchancy'}
                ])

    def test_delete_session(self):
        """
        Ensure we can delete an existing session.
        """

        # DELETE the session you just created
        response = self.client.delete(f"/sessions/{self.session.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the session again to verify you get a 404 response
        response = self.client.get(f"/sessions/{self.session.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
