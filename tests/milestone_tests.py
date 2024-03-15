import json
from rest_framework import status
from rest_framework.test import APITestCase
from kingdomdeathapi.models import Player, Milestone
from rest_framework.authtoken.models import Token


class MilestoneTests(APITestCase):

    fixtures = ['users', 'tokens', 'players', 'settlements', 'milestones', 'milestone_types']

    def setUp(self):
        # Try to retrieve the first existing Player object
        self.player = Player.objects.first()
        # Create a Token for the user if it doesn't exist
        token, created = Token.objects.get_or_create(user=self.player.user)
        # Set the client's credentials using the Token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        # Try to retrieve the first existing Milestone object
        self.milestone = Milestone.objects.first()

    def test_create_milestone(self):
        """
        Ensure we can create a new milestone.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/milestones"

        # Define the request body
        data = {
            "settlement": 1,
            "milestone_type": 4,
            "achieved": True
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(
            json_response["settlement"], 1)
        self.assertEqual(json_response["milestone_type"], {'id': 4, 'type': 'Innovations Reaches 5'})
        self.assertEqual(json_response["achieved"], True)

    def test_get_milestone(self):
        """
        Ensure we can get an existing milestone
        """

        # Initiate request and store response
        response = self.client.get(f"/milestones/{self.milestone.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the milestone was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(
            json_response["settlement"], 2)
        self.assertEqual(json_response["milestone_type"], {'id': 1, 'type': 'First Child Born'})
        self.assertEqual(json_response["achieved"], True)

    def test_change_milestone(self):
        """
        Ensure we can change an existing milestone.
        """

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "settlement": 1,
            "milestone_type": 4,
            "achieved": False,
        }

        response = self.client.put(
            f"/milestones/{self.milestone.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET milestone again to verify changes were made
        response = self.client.get(f"/milestones/{self.milestone.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json_response["settlement"], 1)
        self.assertEqual(json_response["milestone_type"], {'id': 4, 'type': 'Innovations Reaches 5'})
        self.assertEqual(json_response["achieved"], False)

    def test_delete_milestone(self):
        """
        Ensure we can delete an existing milestone.
        """

        # DELETE the milestone you just created
        response = self.client.delete(f"/milestones/{self.milestone.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the milestone again to verify you get a 404 response
        response = self.client.get(f"/milestones/{self.milestone.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
