import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from kingdomdeathapi.models import Player, Survivor, WeaponProficiency, FightingArt, Disorder, Ability
from rest_framework.authtoken.models import Token


class SurvivorTests(APITestCase):

    fixtures = ['users', 'tokens', 'players', 'survivors', 'weapon_proficiencies', 'fighting_arts', 'disorders', 'abilities']

    def setUp(self):
        # Try to retrieve the first existing Player object
        self.player = Player.objects.first()
        # Create a Token for the user if it doesn't exist
        token, created = Token.objects.get_or_create(user=self.player.user)
        # Set the client's credentials using the Token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        # Try to retrieve the first existing Survivor object
        self.survivor = Survivor.objects.first()

    def test_create_survivor(self):
        """
        Ensure we can create a new survivor.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/survivors"

        # Define the request body
        data = {
        "user": 1,
        "name": "Test",
        "survival": 1,
        "insanity": 3,
        "hunt_experience": 1,
        "gender": "Male",
        "movement": 5,
        "accuracy": 0,
        "strength": 0,
        "evasion": 0,
        "speed": 0,
        "luck": 0,
        "understanding": 1,
        "courage": 2,
        "head_armor": 2,
        "head_wound": False,
        "arm_armor": 2,
        "arm_light_wound": True,
        "arm_heavy_wound": False,
        "body_armor": 2,
        "body_light_wound": False,
        "body_heavy_wound": False,
        "waist_armor": 2,
        "waist_light_wound": False,
        "waist_heavy_wound": False,
        "leg_armor": 2,
        "leg_light_wound": True,
        "leg_heavy_wound": False,
        "weapon_proficiency": [8],
        "fighting_art": [1, 3, 9],
        "disorder": [1, 4, 10],
        "ability": [4, 5, 9]
    }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the survivor was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["id"], 8)
        self.assertEqual(json_response["name"], "Test")
        self.assertEqual(json_response["survival"], 1)
        self.assertEqual(json_response["insanity"], 3)
        self.assertEqual(json_response["hunt_experience"], 1)
        self.assertEqual(json_response["gender"], "Male")
        self.assertEqual(json_response["movement"], 5)
        self.assertEqual(json_response["accuracy"], 0)
        self.assertEqual(json_response["strength"], 0)
        self.assertEqual(json_response["evasion"], 0)
        self.assertEqual(json_response["speed"], 0)
        self.assertEqual(json_response["luck"], 0)
        self.assertEqual(json_response["understanding"], 1)
        self.assertEqual(json_response["courage"], 2)
        self.assertEqual(json_response["head_armor"], 2)
        self.assertEqual(json_response["head_wound"], False)
        self.assertEqual(json_response["arm_armor"], 2)
        self.assertEqual(json_response["arm_light_wound"], True)
        self.assertEqual(json_response["arm_heavy_wound"], False)
        self.assertEqual(json_response["body_armor"], 2)
        self.assertEqual(json_response["body_light_wound"], False)
        self.assertEqual(json_response["body_heavy_wound"], False)
        self.assertEqual(json_response["waist_armor"], 2)
        self.assertEqual(json_response["waist_light_wound"], False)
        self.assertEqual(json_response["waist_heavy_wound"], False)
        self.assertEqual(json_response["leg_armor"], 2)
        self.assertEqual(json_response["leg_light_wound"], True)
        self.assertEqual(json_response["leg_heavy_wound"], False)
        self.assertEqual(
            json_response["user"], {'id': 1, 'username': 'Twiknight'})
        self.assertEqual(
            json_response["weapon_proficiency"], [{'id': 8, 'name': 'Shield'}])
        self.assertEqual(
            json_response["fighting_art"],
            [{ "id": 1, "name": "Ambidextrous"},
            { "id": 3, "name": "Clutch Fighter"},
            { "id": 9, "name": "Last Man Standing"}])
        self.assertEqual(
            json_response["disorder"],
            [{ "id": 1, "name": "Aichmophobia"},
            { "id": 4, "name": "Binge Eating"},
            {"id": 10, "name": "Traumatized"}])
        self.assertEqual(
            json_response["ability"],
            [{ "id": 4, "name": "Bitter Frenzy"},
            { "id": 5, "name": "Crystal Skin"},
            { "id": 9, "name": "Oracle's Eye"}])

    def test_get_survivor(self):
        """
        Ensure we can get an existing survivor
        """

        # Initiate request and store response
        response = self.client.get(f"/survivors/{self.survivor.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the survivor was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["name"], "Yharnam")
        self.assertEqual(json_response["survival_limit"], 4)
        self.assertEqual(json_response["population"], 3)
        self.assertEqual(
            json_response["game_master"], {'id': 1, 'username': 'Twiknight'})

    def test_change_survivor(self):
        """
        Ensure we can change an existing survivor.
        """

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "name": "New",
            "survival_limit": 4,
            "population": 10,
            "game_master": self.player.id
        }

        response = self.client.put(
            f"/survivors/{self.survivor.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET survivor again to verify changes were made
        response = self.client.get(f"/survivors/{self.survivor.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "New")
        self.assertEqual(json_response["survival_limit"], 4)
        self.assertEqual(json_response["population"], 10)
        self.assertEqual(json_response["game_master"], {'id': 1, 'username': 'Twiknight'})

    def test_delete_survivor(self):
        """
        Ensure we can delete an existing survivor.
        """

        # DELETE the survivor you just created
        response = self.client.delete(f"/survivors/{self.survivor.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the survivor again to verify you get a 404 response
        response = self.client.get(f"/survivors/{self.survivor.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
