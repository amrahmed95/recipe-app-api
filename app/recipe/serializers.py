"""
Serializers for recipe APIs
"""
from rest_framework import serializers
from core.models import (
    Recipe,
    Tag,
    Ingredient
)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags',
                  'ingredients']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create and return a new recipe."""
        # Extract tags and Ingredients Data
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])

        # Set the authenticated user from the request
        request = self.context.get('request')
        validated_data['user'] = request.user

        # Create the recipe
        recipe = Recipe.objects.create(**validated_data)

        # Create or get tags and associate them with the recipe
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=request.user,
                **tag
            )
            recipe.tags.add(tag_obj)

        # Create or get ingredients and associate them with the recipe
        for ingredient_data in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=request.user,
                name=ingredient_data['name']
            )
            recipe.ingredients.add(ingredient_obj)

        return recipe

    def update(self, instance, validated_data):
        """Update and return a recipe."""
        # Extract tags and Ingredients Data
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)

        # Update the recipe
        recipe = super().update(instance, validated_data)

        # Set the authenticated user from the request
        request = self.context.get('request')
        validated_data['user'] = request.user

        # Create or get tags and associate them with the recipe
        if tags is not None:
            recipe.tags.clear()
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(
                    user=request.user,
                    **tag
                )
                recipe.tags.add(tag_obj)

        # Create or get ingredients and associate them with the recipe
        if ingredients is not None:
            recipe.ingredients.clear()
            for ingredient in ingredients:
                ingredients_obj, created = Ingredient.objects.get_or_create(
                    user=request.user,
                    **ingredient
                )
                recipe.ingredients.add(ingredients_obj)

        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
