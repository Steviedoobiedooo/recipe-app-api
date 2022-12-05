"""
Django Admin Customization for Recipe
"""
from django.contrib import admin
from recipe import models
from django.utils.html import mark_safe


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'time_minutes',
        'price',
        'link'
    ]

    def get_image(self, obj):
        image = obj.data

        if not image:
            return

        return mark_safe(
            '<a href="{url}" target="_blank"><img src="{url}"/></a>'
            .format(url=image.url)
        )

    get_image.short_description = 'Image'


admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
