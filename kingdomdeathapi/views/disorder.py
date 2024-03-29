from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from kingdomdeathapi.models import Disorder, ExpansionType


class DisorderView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of disorders based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        disorders = Disorder.objects.all()

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
                    disorders = disorders.filter(expansion=expansion_id)
                else:
                    disorders = disorders.exclude(expansion=expansion_id)

        if request.query_params.get('expansion') is not None:
            if request.query_params.get('expansion') == 'true':
                # The Q() syntax selects objects that follow the expression within the brackets. The ~ negates the expression
                disorders = disorders.filter(~Q(expansion=None))
            if request.query_params.get('expansion') == 'false':
                disorders = disorders.filter(expansion__isnull=True)

        serializer = DisorderSerializer(disorders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific disorder by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the disorder to retrieve.

        Returns:
            Response: A serialized dictionary containing the disorder's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the disorder with the specified primary key does not exist.
        """
        try:
            disorder = Disorder.objects.get(pk=pk)
            serializer = DisorderSerializer(disorder, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Disorder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the disorder to retrieve.

        Returns:
            Response: A serialized dictionary containing the disorder's data and HTTP status 201 Created.
        """

        disorder = Disorder.objects.create(
            name=request.data["name"]
        )

        serializer = DisorderSerializer(disorder, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific disorder's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the disorder to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the disorder's user details,
            or HTTP status 404 Not Found if the disorder with the specified primary key does not exist.
        """
        try:
            disorder = Disorder.objects.get(pk=pk)
            disorder.name = request.data["name"]
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Disorder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific disorder and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the disorder to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the disorder with the specified primary key does not exist.
        """

        try:
            disorder = Disorder.objects.get(pk=pk)
            disorder.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Disorder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class ExpansionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpansionType
        fields = ('id', 'name',)


class DisorderSerializer(serializers.ModelSerializer):

    expansion = ExpansionTypeSerializer(many=False)

    class Meta:
        model = Disorder
        fields = ('id', 'name', 'flavor_text', 'effect', 'expansion')
