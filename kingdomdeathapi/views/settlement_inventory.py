from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import SettlementInventory, Settlement, Resource, ResourceType


class SettlementInventoryView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of settlement_inventories based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        settlement_inventories = SettlementInventory.objects.all()

        if "settlement" in request.query_params:
            settlement_value = request.query_params.get('settlement')
            settlement_inventories = settlement_inventories.filter(settlement=settlement_value)

        serializer = SettlementInventorySerializer(settlement_inventories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific settlement_inventory by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the settlement_inventory to retrieve.

        Returns:
            Response: A serialized dictionary containing the settlement_inventory's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the settlement_inventory with the specified primary key does not exist.
        """
        try:
            settlement_inventory = SettlementInventory.objects.get(pk=pk)
            serializer = SettlementInventorySerializer(settlement_inventory, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SettlementInventory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the settlement_inventory to retrieve.

        Returns:
            Response: A serialized dictionary containing the settlement_inventory's data and HTTP status 201 Created.
        """
        settlement = Settlement.objects.get(pk=request.data["settlement"])
        resource = Resource.objects.get(pk=request.data["resource"])

        settlement_inventory = SettlementInventory.objects.create(
            settlement=settlement,
            resource=resource,
            amount=request.data["amount"],
        )

        serializer = SettlementInventorySerializer(settlement_inventory, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific settlement_inventory's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the settlement_inventory to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the settlement_inventory's user details,
            or HTTP status 404 Not Found if the settlement_inventory with the specified primary key does not exist.
        """
        try:
            settlement_inventory = SettlementInventory.objects.get(pk=pk)
            settlement_inventory.amount = request.data["amount"]
            settlement_inventory.resource = Resource.objects.get(
                pk=request.data["resource"])
            settlement_inventory.settlement = Settlement.objects.get(
                pk=request.data["settlement"])
            settlement_inventory.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except SettlementInventory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific settlement_inventory and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the settlement_inventory to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the settlement_inventory with the specified primary key does not exist.
        """

        try:
            settlement_inventory = SettlementInventory.objects.get(pk=pk)
            settlement_inventory.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except SettlementInventory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ResourceSerializer(serializers.ModelSerializer):

    class ResourceTypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = ResourceType
            fields = ('id', 'name', )

    type = ResourceTypeSerializer(many=False)

    class Meta:
        model = Resource
        fields = ('id', 'name', 'type', )

class SettlementInventorySerializer(serializers.ModelSerializer):

    resource = ResourceSerializer(many=False)

    class Meta:
        model = SettlementInventory
        fields = ('id', 'settlement', 'resource', 'amount', )
