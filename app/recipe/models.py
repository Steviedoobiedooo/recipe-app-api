import uuid
import os
from django.db import models
from django.conf import settings


def recipe_image_file_path(instance, filename):
    """
    Generate file path for new recipe image
    """

    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid5(uuid.uuid4(), filename)}{ext}'

    return os.path.join('uploads', 'recipe', filename)


class Recipe(models.Model):
    """
    Recipe object
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Tag object for filtering recipes
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Ingredient object
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
