from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from kingdomdeathapi.models import Resource, ResourceType, Monster, ExpansionType


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

        # Define a dictionary mapping query parameters to type IDs
        type_mappings = {
            "hide": 1,
            "bone": 2,
            "organ": 3,
            "scrap": 4,
            "herb": 5,
            "iron": 6,
            "vermin": 7,
            "flower": 8
        }

        # Iterate over the dictionary and apply filters
        for param, type_id in type_mappings.items():
            if request.query_params.get(param) is not None:
                value = request.query_params.get(param) == 'true'
                if value:
                    resources = resources.filter(type__id=type_id)
                else:
                    resources = resources.exclude(type__id=type_id)

        bool_mappings = {
            "consumable": True,
            "monster": True,
            "strange": True,
            "indomitable": True
        }

        for param, bool_value in bool_mappings.items():
            if request.query_params.get(param) is not None:
                value = request.query_params.get(param) == 'true'
                if value:
                    resources = resources.filter(**{f"{param}": bool_value})
                else:
                    resources = resources.exclude(**{f"{param}": bool_value})

        monster_mappings = {
            "white_lion": 1,
            "screaming_antelope": 2,
            "phoenix": 3,
            "dragon_king": 9,
            "dung_beetle_knight": 11,
        }

        for param, monster_id in monster_mappings.items():
            if request.query_params.get(param) is not None:
                value = request.query_params.get(param) == 'true'
                if value:
                    resources = resources.filter(monster_origin=monster_id)
                else:
                    resources = resources.exclude(monster_origin=monster_id)

        expansion_mappings = {
            "dragon_king_exp": 1,
            "dung_beetle_knight_exp": 2,
            "flower_knight_exp": 3,
            "gorm_exp": 4,
            "lion_god_exp": 5,
            "lion_knight_exp": 6,
            "lonely_tree_exp": 7,
            "manhunter_exp": 8,
            "slenderman_exp": 9,
            "spidicules_exp": 10,
            "sunstalker_exp": 11,
            "gamblers_chest_exp": 12
        }

        for param, expansion_id in expansion_mappings.items():
            if request.query_params.get(param) is not None:
                value = request.query_params.get(param) == 'true'
                if value:
                    resources = resources.filter(expansion=expansion_id)
                else:
                    resources = resources.exclude(expansion=expansion_id)


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

class MonsterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monster
        fields = ('id', 'name',)

class ExpansionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpansionType
        fields = ('id', 'name',)


class ResourceSerializer(serializers.ModelSerializer):

    type = ResourceTypeSerializer(many=True)
    monster_origin = MonsterSerializer(many=False)
    expansion = ExpansionTypeSerializer(many=False)

    class Meta:
        model = Resource
        fields = ('id', 'name', 'type', 'consumable', 'monster', 'strange', 'indomitable', 'monster_origin', 'expansion', 'flavor_text', 'effect')
