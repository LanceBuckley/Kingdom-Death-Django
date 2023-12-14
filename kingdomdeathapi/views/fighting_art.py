from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import FightingArt


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


class FightingArtSerializer(serializers.ModelSerializer):

    class Meta:
        model = FightingArt
        fields = ('id', 'name', )
