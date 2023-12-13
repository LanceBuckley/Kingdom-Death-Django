from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import Resource, ResourceType


class ResourceView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of resources based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        resources = Resource.objects.all()

        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific resource by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the resource to retrieve.

        Returns:
            Response: A serialized dictionary containing the resource's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the resource with the specified primary key does not exist.
        """
        try:
            resource = Resource.objects.get(pk=pk)
            serializer = ResourceSerializer(resource, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Resource.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the resource to retrieve.

        Returns:
            Response: A serialized dictionary containing the resource's data and HTTP status 201 Created.
        """
        type = ResourceType.objects.get(pk=request.data["type"])

        resource = Resource.objects.create(
            name=request.data["name"],
            type=type
        )

        serializer = ResourceSerializer(resource, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific resource's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the resource to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the resource's user details,
            or HTTP status 404 Not Found if the resource with the specified primary key does not exist.
        """
        try:
            resource = Resource.objects.get(pk=pk)
            resource.name = request.data["name"]
            resource.type = ResourceType.objects.get(
                pk=request.data["type"])
            resource.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Resource.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific resource and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the resource to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the resource with the specified primary key does not exist.
        """

        try:
            resource = Resource.objects.get(pk=pk)
            resource.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Resource.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = ('id', 'name',)


class ResourceSerializer(serializers.ModelSerializer):

    type = ResourceTypeSerializer(many=False)

    class Meta:
        model = Resource
        fields = ('id', 'name', 'type',)
