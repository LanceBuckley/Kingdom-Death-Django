from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from kingdomdeathapi.models import FightingArt, ExpansionType


class FightingArtView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of fighting_arts based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        fighting_arts = FightingArt.objects.all()

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
                    fighting_arts = fighting_arts.filter(expansion=expansion_id)
                else:
                    fighting_arts = fighting_arts.exclude(expansion=expansion_id)

        if request.query_params.get('expansion') is not None:
            if request.query_params.get('expansion') == 'true':
                # The Q() syntax selects objects that follow the expression within the brackets. The ~ negates the expression
                fighting_arts = fighting_arts.filter(~Q(expansion=None))
            if request.query_params.get('expansion') == 'false':
                fighting_arts = fighting_arts.filter(expansion__isnull=True)

        serializer = FightingArtSerializer(fighting_arts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific fighting_art by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the fighting_art to retrieve.

        Returns:
            Response: A serialized dictionary containing the fighting_art's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the fighting_art with the specified primary key does not exist.
        """
        try:
            fighting_art = FightingArt.objects.get(pk=pk)
            serializer = FightingArtSerializer(fighting_art, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FightingArt.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the fighting_art to retrieve.

        Returns:
            Response: A serialized dictionary containing the fighting_art's data and HTTP status 201 Created.
        """

        fighting_art = FightingArt.objects.create(
            name=request.data["name"]
        )

        serializer = FightingArtSerializer(fighting_art, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific fighting_art's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the fighting_art to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the fighting_art's user details,
            or HTTP status 404 Not Found if the fighting_art with the specified primary key does not exist.
        """
        try:
            fighting_art = FightingArt.objects.get(pk=pk)
            fighting_art.name = request.data["name"]
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except FightingArt.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific fighting_art and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the fighting_art to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the fighting_art with the specified primary key does not exist.
        """

        try:
            fighting_art = FightingArt.objects.get(pk=pk)
            fighting_art.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except FightingArt.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class ExpansionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpansionType
        fields = ('id', 'name',)


class FightingArtSerializer(serializers.ModelSerializer):

    expansion = ExpansionTypeSerializer(many=False)

    class Meta:
        model = FightingArt
        fields = ('id', 'name', 'effect', 'expansion')
