from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import Player


class PlayerView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of players based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        players = Player.objects.all()

        if request.query_params.get('game_master') is not None:
            if request.query_params.get('game_master') == 'true':
                players = players.filter(game_master=True)
            elif request.query_params.get('game_master') == 'false':
                players = players.filter(game_master=False)

        if "current" in request.query_params:
            players = players.filter(user=request.auth.user)

        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific player by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the player to retrieve.

        Returns:
            Response: A serialized dictionary containing the player's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the player with the specified primary key does not exist.
        """
        try:
            player = Player.objects.get(pk=pk)
            serializer = PlayerSerializer(player, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific player's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the player to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the player's user details,
            or HTTP status 404 Not Found if the player with the specified primary key does not exist.
        """
        try:
            player = Player.objects.get(pk=pk)
            player.user.first_name = request.data["first_name"]
            player.user.last_name = request.data["last_name"]
            player.user.username = request.data["username"]
            player.user.email = request.data["email"]
            player.user.save()
            player.game_master = request.data["game_master"]
            player.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific player and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the player to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the player with the specified primary key does not exist.
        """

        try:
            player = Player.objects.get(pk=pk)
            user = player.user
            player.delete()
            user.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'game_master', 'full_name')
