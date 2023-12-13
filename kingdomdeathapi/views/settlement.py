from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import Settlement, Player


class SettlementView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of settlements based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        settlements = Settlement.objects.all()

        serializer = SettlementSerializer(settlements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific settlement by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the settlement to retrieve.

        Returns:
            Response: A serialized dictionary containing the settlement's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the settlement with the specified primary key does not exist.
        """
        try:
            settlement = Settlement.objects.get(pk=pk)
            serializer = SettlementSerializer(settlement, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Settlement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the settlement to retrieve.

        Returns:
            Response: A serialized dictionary containing the settlement's data and HTTP status 201 Created.
        """
        game_master = Player.objects.get(pk=request.data["game_master"])

        settlement = Settlement.objects.create(
            name=request.data["name"],
            survival_limit=request.data["survival_limit"],
            population=request.data["population"],
            game_master=game_master
        )

        serializer = SettlementSerializer(settlement, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific settlement's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the settlement to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the settlement's user details,
            or HTTP status 404 Not Found if the settlement with the specified primary key does not exist.
        """
        try:
            settlement = Settlement.objects.get(pk=pk)
            settlement.name = request.data["name"]
            settlement.survival_limit = request.data["survival_limit"]
            settlement.population = request.data["population"]
            settlement.game_master = Player.objects.get(
                pk=request.data["game_master"])
            settlement.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Settlement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific settlement and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the settlement to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the settlement with the specified primary key does not exist.
        """

        try:
            settlement = Settlement.objects.get(pk=pk)
            settlement.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Settlement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'username',)

class SettlementSerializer(serializers.ModelSerializer):

    game_master = PlayerSerializer(many=False)

    class Meta:
        model = Settlement
        fields = ('id', 'name', 'population', 'survival_limit', 'game_master',)
