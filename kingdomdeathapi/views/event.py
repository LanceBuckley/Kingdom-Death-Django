from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import Event


class EventView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of events based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        events = Event.objects.all()

        serializer = EventSerializer(events, many=True)
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
            ability = Event.objects.get(pk=pk)
            serializer = EventSerializer(ability, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
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

        ability = Event.objects.create(
            name=request.data["name"]
        )

        serializer = EventSerializer(ability, many=False)
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
            ability = Event.objects.get(pk=pk)
            ability.name = request.data["name"]
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
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
            ability = Event.objects.get(pk=pk)
            ability.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'name', )
