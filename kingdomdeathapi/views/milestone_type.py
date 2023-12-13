from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import MilestoneType


class MilestoneTypeView(ViewSet):

    def list(self, request):
        """
        Summary:
            Retrieve a list of milestones based on query parameters.

        Args:
            request (HttpRequest): The full HTTP request object.

        Returns:
            Response: A serialized dictionary and HTTP status 200 OK.
        """
        milestones = MilestoneType.objects.all()

        serializer = MilestoneSerializer(milestones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MilestoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = MilestoneType
        fields = ('id', 'type',)
