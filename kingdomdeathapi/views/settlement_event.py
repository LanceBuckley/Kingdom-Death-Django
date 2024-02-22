from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import SettlementEvent, Settlement, Event


class SettlementEventView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of settlement_events based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        settlement_events = SettlementEvent.objects.all()

        if "settlement" in request.query_params:
            settlement_value = request.query_params.get('settlement')
            settlement_events = settlement_events.filter(settlement=settlement_value)


        serializer = SettlementEventSerializer(settlement_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific settlement_event by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the settlement_event to retrieve.

        Returns:
            Response: A serialized dictionary containing the settlement_event's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the settlement_event with the specified primary key does not exist.
        """
        try:
            settlement_event = SettlementEvent.objects.get(pk=pk)
            serializer = SettlementEventSerializer(settlement_event, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SettlementEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the settlement_event to retrieve.

        Returns:
            Response: A serialized dictionary containing the settlement_event's data and HTTP status 201 Created.
        """
        settlement = Settlement.objects.get(pk=request.data["settlement"])
        event = Event.objects.get(pk=request.data["event"])

        settlement_event = SettlementEvent.objects.create(
            settlement=settlement,
            event=event,
            year=request.data["year"],
        )

        serializer = SettlementEventSerializer(settlement_event, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific settlement_event's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the settlement_event to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the settlement_event's user details,
            or HTTP status 404 Not Found if the settlement_event with the specified primary key does not exist.
        """
        try:
            settlement_event = SettlementEvent.objects.get(pk=pk)
            settlement_event.year = request.data["year"]
            settlement_event.event = Event.objects.get(
                pk=request.data["event"])
            settlement_event.settlement = Settlement.objects.get(
                pk=request.data["settlement"])
            settlement_event.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except SettlementEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific settlement_event and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the settlement_event to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the settlement_event with the specified primary key does not exist.
        """

        try:
            settlement_event = SettlementEvent.objects.get(pk=pk)
            settlement_event.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except SettlementEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'name', )

class SettlementEventSerializer(serializers.ModelSerializer):

    event = EventSerializer(many=False)

    class Meta:
        model = SettlementEvent
        fields = ('id', 'settlement', 'event', 'year', )
