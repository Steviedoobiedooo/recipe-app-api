"""
Serializers for the recipe API View
"""
from .models import (Recipe, Tag, Ingredient)
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the tag object
    """

    class Meta:
        model = Tag
        fields = [
            'id',
            'name'
        ]
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for ingredient object
    """

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name'
        ]
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the recipe object
    """

    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'time_minutes',
            'price',
            'link',
            'tags',
            'ingredients'
        ]
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """
        Handle getting or creating tags as needed
        """

        auth_user = self.context['request'].user

        for tag in tags:
            obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """
        Handle getting or creating ingredients as needed
        """

        auth_user = self.context['request'].user

        for ingredient in ingredients:
            obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(obj)

    def create(self, validated_data):
        """
        Create a recipe link tags and ingredients to it
        """

        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """
        Update recipe object
        """

        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """
    Serializer for recipe detail view
    """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description', 'image']


class RecipeImageSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading image to recipes
    """

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}
