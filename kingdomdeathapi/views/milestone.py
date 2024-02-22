from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import Milestone, Settlement, MilestoneType


class MilestoneView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of milestones based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        milestones = Milestone.objects.all()

        if "achieved" in request.query_params:
            achieved_value = request.query_params.get('achieved')
            milestones = milestones.filter(achieved=achieved_value)

        if "settlement" in request.query_params:
            settlement_value = request.query_params.get('settlement')
            milestones = milestones.filter(settlement=settlement_value)


        serializer = MilestoneSerializer(milestones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Summary:
            Retrieve a specific milestone by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the milestone to retrieve.

        Returns:
            Response: A serialized dictionary containing the milestone's data and HTTP status 200 OK,
            or HTTP status 404 Not Found if the milestone with the specified primary key does not exist.
        """
        try:
            milestone = Milestone.objects.get(pk=pk)
            serializer = MilestoneSerializer(milestone, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Milestone.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Summary:
            Create a new object using the request data

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the milestone to retrieve.

        Returns:
            Response: A serialized dictionary containing the milestone's data and HTTP status 201 Created.
        """
        settlement = Settlement.objects.get(pk=request.data["settlement"])
        milestone_type = MilestoneType.objects.get(pk=request.data["milestone_type"])

        milestone = Milestone.objects.create(
            settlement=settlement,
            milestone_type=milestone_type,
            achieved=request.data["achieved"],
        )

        serializer = MilestoneSerializer(milestone, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Summary:
            Update a specific milestone's user information by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the milestone to update.

        Returns:
            Response: A successful HTTP status 204 No Content response after updating the milestone's user details,
            or HTTP status 404 Not Found if the milestone with the specified primary key does not exist.
        """
        try:
            milestone = Milestone.objects.get(pk=pk)
            milestone.achieved = request.data["achieved"]
            milestone.milestone_type = MilestoneType.objects.get(
                pk=request.data["milestone_type"])
            milestone.settlement = Settlement.objects.get(
                pk=request.data["settlement"])
            milestone.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Milestone.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Summary:
            Delete a specific milestone and associated user by primary key.

        Args:
            request (HttpRequest): The full HTTP request object.
            pk (int): The primary key of the milestone to delete.

        Returns:
            Response: A successful HTTP status 204 No Content response after deletion,
            or HTTP status 404 Not Found if the milestone with the specified primary key does not exist.
        """

        try:
            milestone = Milestone.objects.get(pk=pk)
            milestone.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Milestone.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class MilestoneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilestoneType
        fields = ('id', 'type', )

class MilestoneSerializer(serializers.ModelSerializer):

    milestone_type = MilestoneTypeSerializer(many=False)

    class Meta:
        model = Milestone
        fields = ('id', 'settlement', 'milestone_type', 'achieved', )
