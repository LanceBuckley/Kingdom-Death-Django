from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import Session, Player, Settlement


class SessionView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of sessions based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        sessions = Session.objects.all()

        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific session by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the session to retrieve.

        Returns:
            Response: A serialized dictionary containing the session's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the session with the specified primary key does not exist.
        """
        try:
            session = Session.objects.get(pk=pk)
            serializer = SessionSerializer(session, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Session.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the session to retrieve.

        Returns:
            Response: A serialized dictionary containing the session's data and HTTP status 201 Created.
        """
        host = Player.objects.get(pk=request.data["host"])
        settlement = Settlement.objects.get(pk=request.data["settlement"])
        players = Player.objects.filter(pk__in=request.data["players"])

        session = Session.objects.create(
            host=host,
            settlement=settlement
        )

        session.players.set(players)

        serializer = SessionSerializer(session, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific session's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the session to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the session's user details,
            or HTTP status 404 Not Found if the session with the specified primary key does not exist.
        """
        try:
            session = Session.objects.get(pk=pk)
            players = Player.objects.filter(pk__in=request.data["players"])
            session.host = Player.objects.get(
                pk=request.data["host"])
            session.players.set(players)
            session.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Session.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific session and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the session to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the session with the specified primary key does not exist.
        """

        try:
            session = Session.objects.get(pk=pk)
            session.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Session.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'username',)

class SessionSerializer(serializers.ModelSerializer):

    host = PlayerSerializer(many=False)
    players = PlayerSerializer(many=True)

    class Meta:
        model = Session
        fields = ('id', 'host', 'settlement', 'players')
