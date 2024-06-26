from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from kingdomdeathapi.models import WeaponProficiency, ExpansionType


class WeaponProficiencyView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of weapon_proficiencies based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        weapon_proficiencies = WeaponProficiency.objects.all()

        expansion_mappings = {
            "dragon_king_exp": 1,
            "dung_beetle_knight_exp": 2,
            "flower_knight_exp": 3,
            "gorm_exp": 4,
            "lion_god_exp": 5,
            "lion_knight_exp": 6,
            "lonely_tree_exp": 7,
            "manhunter_exp": 8,
            "slenderman_exp": 9,
            "spidicules_exp": 10,
            "sunstalker_exp": 11,
            "gamblers_chest_exp": 12
        }

        for param, expansion_id in expansion_mappings.items():
            if request.query_params.get(param) is not None:
                value = request.query_params.get(param) == 'true'
                if value:
                    weapon_proficiencies = weapon_proficiencies.filter(expansion=expansion_id)
                else:
                    weapon_proficiencies = weapon_proficiencies.exclude(expansion=expansion_id)

        if request.query_params.get('expansion') is not None:
            if request.query_params.get('expansion') == 'true':
                # The Q() syntax selects objects that follow the expression within the brackets. The ~ negates the expression
                weapon_proficiencies = weapon_proficiencies.filter(~Q(expansion=None))
            if request.query_params.get('expansion') == 'false':
                weapon_proficiencies = weapon_proficiencies.filter(expansion__isnull=True)

        serializer = WeaponProficiencySerializer(weapon_proficiencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific weapon_proficiency by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the weapon_proficiency to retrieve.

        Returns:
            Response: A serialized dictionary containing the weapon_proficiency's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the weapon_proficiency with the specified primary key does not exist.
        """
        try:
            weapon_proficiency = WeaponProficiency.objects.get(pk=pk)
            serializer = WeaponProficiencySerializer(weapon_proficiency, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except WeaponProficiency.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the weapon_proficiency to retrieve.

        Returns:
            Response: A serialized dictionary containing the weapon_proficiency's data and HTTP status 201 Created.
        """

        weapon_proficiency = WeaponProficiency.objects.create(
            name=request.data["name"]
        )

        serializer = WeaponProficiencySerializer(weapon_proficiency, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific weapon_proficiency's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the weapon_proficiency to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the weapon_proficiency's user details,
            or HTTP status 404 Not Found if the weapon_proficiency with the specified primary key does not exist.
        """
        try:
            weapon_proficiency = WeaponProficiency.objects.get(pk=pk)
            weapon_proficiency.name = request.data["name"]
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except WeaponProficiency.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific weapon_proficiency and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the weapon_proficiency to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the weapon_proficiency with the specified primary key does not exist.
        """

        try:
            weapon_proficiency = WeaponProficiency.objects.get(pk=pk)
            weapon_proficiency.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except WeaponProficiency.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class ExpansionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpansionType
        fields = ('id', 'name',)


class WeaponProficiencySerializer(serializers.ModelSerializer):

    class Meta:
        model = WeaponProficiency
        fields = ('id', 'name', 'specialist_effect', 'master_effect', 'expansion')
