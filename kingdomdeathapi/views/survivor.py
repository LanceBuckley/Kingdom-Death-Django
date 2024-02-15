from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import Survivor, Player, WeaponProficiency, FightingArt, Ability, Disorder


class SurvivorView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of survivors based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        survivors = Survivor.objects.all()

        serializer = SurvivorSerializer(survivors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific survivor by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the survivor to retrieve.

        Returns:
            Response: A serialized dictionary containing the survivor's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the survivor with the specified primary key does not exist.
        """
        try:
            survivor = Survivor.objects.get(pk=pk)
            serializer = SurvivorSerializer(survivor, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Survivor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the survivor to retrieve.

        Returns:
            Response: A serialized dictionary containing the survivor's data and HTTP status 201 Created.
        """
        user = Player.objects.get(pk=request.data["user"])
        weapon_proficiency = WeaponProficiency.objects.get(pk=request.data["weapon_proficiency"])
        fighting_art = FightingArt.objects.get(pk=request.data["fighting_art"])
        disorder = Disorder.objects.get(pk=request.data["disorder"])
        ability = Ability.objects.get(pk=request.data["ability"])


        survivor = Survivor.objects.create(
            name=request.data["name"],
            survival=request.data["survival"],
            insanity=request.data["insanity"],
            hunt_experience=request.data["hunt_experience"],
            gender=request.data["gender"],
            movement=request.data["movement"],
            accuracy=request.data["accuracy"],
            strength=request.data["strength"],
            evasion=request.data["evasion"],
            speed=request.data["speed"],
            luck=request.data["luck"],
            understanding=request.data["understanding"],
            courage=request.data["courage"],
            head_armor=request.data["head_armor"],
            head_wound=request.data["head_wound"],
            arm_armor=request.data["arm_armor"],
            arm_light_wound=request.data["arm_light_wound"],
            arm_heavy_wound=request.data["arm_heavy_wound"],
            body_armor=request.data["body_armor"],
            body_light_wound=request.data["body_light_wound"],
            body_heavy_wound=request.data["body_heavy_wound"],
            waist_armor=request.data["waist_armor"],
            waist_light_wound=request.data["waist_light_wound"],
            waist_heavy_wound=request.data["waist_heavy_wound"],
            leg_armor=request.data["leg_armor"],
            leg_light_wound=request.data["leg_light_wound"],
            leg_heavy_wound=request.data["leg_heavy_wound"],
            user=user,
            weapon_proficiency = weapon_proficiency,
            fighting_art = fighting_art,
            disorder = disorder,
            ability = ability
        )

        serializer = SurvivorSerializer(survivor, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific survivor's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the survivor to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the survivor's user details,
            or HTTP status 404 Not Found if the survivor with the specified primary key does not exist.
        """
        try:
            survivor = Survivor.objects.get(pk=pk)
            survivor.name=request.data["name"],
            survivor.survival=request.data["survival"],
            survivor.insanity=request.data["insanity"],
            survivor.hunt_experience=request.data["hunt_experience"],
            survivor.gender=request.data["gender"],
            survivor.movement=request.data["movement"],
            survivor.accuracy=request.data["accuracy"],
            survivor.strength=request.data["strength"],
            survivor.evasion=request.data["evasion"],
            survivor.speed=request.data["speed"],
            survivor.luck=request.data["luck"],
            survivor.understanding=request.data["understanding"],
            survivor.courage=request.data["courage"],
            survivor.head_armor=request.data["head_armor"],
            survivor.head_wound=request.data["head_wound"],
            survivor.arm_armor=request.data["arm_armor"],
            survivor.arm_light_wound=request.data["arm_light_wound"],
            survivor.arm_heavy_wound=request.data["arm_heavy_wound"],
            survivor.body_armor=request.data["body_armor"],
            survivor.body_light_wound=request.data["body_light_wound"],
            survivor.body_heavy_wound=request.data["body_heavy_wound"],
            survivor.waist_armor=request.data["waist_armor"],
            survivor.waist_light_wound=request.data["waist_light_wound"],
            survivor.waist_heavy_wound=request.data["waist_heavy_wound"],
            survivor.leg_armor=request.data["leg_armor"],
            survivor.leg_light_wound=request.data["leg_light_wound"],
            survivor.leg_heavy_wound=request.data["leg_heavy_wound"],
            survivor.user = Player.objects.get(
                pk=request.data["user"])
            survivor.weapon_proficiency = WeaponProficiency.objects.get(
                pk=request.data["weapon_proficiency"])
            survivor.fighting_art = FightingArt.objects.get(
                pk=request.data["fighting_art"])
            survivor.disorder = Disorder.objects.get(
                pk=request.data["disorder"])
            survivor.ability = Ability.objects.get(
                pk=request.data["ability"])
            survivor.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Survivor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific survivor and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the survivor to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the survivor with the specified primary key does not exist.
        """

        try:
            survivor = Survivor.objects.get(pk=pk)
            survivor.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Survivor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'username',)

class WeaponProficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeaponProficiency
        fields = ('id', 'name',)

class FightingArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = FightingArt
        fields = ('id', 'name',)

class DisorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disorder
        fields = ('id', 'name',)

class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ('id', 'name',)

class SurvivorSerializer(serializers.ModelSerializer):

    user = PlayerSerializer(many=False)
    weapon_proficiency = WeaponProficiencySerializer(many=True)
    fighting_art = FightingArtSerializer(many=True)
    disorder = DisorderSerializer(many=True)
    ability = AbilitySerializer(many=True)

    class Meta:
        model = Survivor
        fields = (
    'id', 'user', 'name', 'survival', 'insanity', 'hunt_experience', 'gender',
    'movement', 'accuracy', 'strength', 'evasion', 'speed', 'luck', 'understanding',
    'courage', 'head_armor', 'head_wound', 'arm_armor', 'arm_light_wound',
    'arm_heavy_wound', 'body_armor', 'body_light_wound', 'body_heavy_wound',
    'waist_armor', 'waist_light_wound', 'waist_heavy_wound', 'leg_armor',
    'leg_light_wound', 'leg_heavy_wound', 'weapon_proficiency', 'fighting_art',
    'disorder', 'ability',
)
