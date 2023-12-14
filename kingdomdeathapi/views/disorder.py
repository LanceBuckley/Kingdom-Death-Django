from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import Disorder


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


class DisorderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disorder
        fields = ('id', 'name', )
