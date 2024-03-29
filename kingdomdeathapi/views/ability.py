from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from kingdomdeathapi.models import Ability, ExpansionType


class AbilityView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of abilities based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        abilities = Ability.objects.all()

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
                    abilities = abilities.filter(expansion=expansion_id)
                else:
                    abilities = abilities.exclude(expansion=expansion_id)

        if request.query_params.get('expansion') is not None:
            if request.query_params.get('expansion') == 'true':
                # The Q() syntax selects objects that follow the expression within the brackets. The ~ negates the expression
                abilities = abilities.filter(~Q(expansion=None))
            if request.query_params.get('expansion') == 'false':
                abilities = abilities.filter(expansion__isnull=True)

        serializer = AbilitySerializer(abilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific ability by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the ability to retrieve.

        Returns:
            Response: A serialized dictionary containing the ability's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the ability with the specified primary key does not exist.
        """
        try:
            ability = Ability.objects.get(pk=pk)
            serializer = AbilitySerializer(ability, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ability.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the ability to retrieve.

        Returns:
            Response: A serialized dictionary containing the ability's data and HTTP status 201 Created.
        """

        ability = Ability.objects.create(
            name=request.data["name"]
        )

        serializer = AbilitySerializer(ability, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific ability's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the ability to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the ability's user details,
            or HTTP status 404 Not Found if the ability with the specified primary key does not exist.
        """
        try:
            ability = Ability.objects.get(pk=pk)
            ability.name = request.data["name"]
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Ability.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific ability and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the ability to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the ability with the specified primary key does not exist.
        """

        try:
            ability = Ability.objects.get(pk=pk)
            ability.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Ability.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
class ExpansionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpansionType
        fields = ('id', 'name',)


class AbilitySerializer(serializers.ModelSerializer):

    expansion = ExpansionTypeSerializer(many=False)

    class Meta:
        model = Ability
        fields = ('id', 'name', 'effect', 'expansion')
