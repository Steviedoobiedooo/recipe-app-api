"""
Tests for tags API
"""
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from recipe.serializers import TagSerializer
from recipe.models import (Tag, Recipe)
from user.tests.test_user_api import create_user

TAGS_URL = reverse('recipe:tag-list')


def detail_url(tag_id):
    """
    Create and return a tag detail url
    """

    return reverse('recipe:tag-detail', args=[tag_id])


class PublicTagsAPITests(TestCase):
    """
    Test unauthenticated API requests
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test auth is required for retrieving tags
        """

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """
    Test authenticated API requests
    """

    def setUp(self):
        self.user = create_user(
            email='user2@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """
        Test retrieving a list of tags
        """

        Tag.objects.create(user=self.user, name='Tag1')
        Tag.objects.create(user=self.user, name='Tag2')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """
        Test list of tags is limited to authenticated user
        """

        user2 = create_user(
            email='user3@example.com',
            password='testpass123'
        )
        Tag.objects.create(user=user2, name='Tag3')
        tag = Tag.objects.create(user=self.user, name='Tag4')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """
        Test updating a tag
        """

        tag = Tag.objects.create(user=self.user, name="After Dinner")

        payload = {'name': 'Dessert'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """
        Test deleting a tag
        """

        tag = Tag.objects.create(user=self.user, name='Breakfast')

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())

    def test_filter_tags_assigned_to_recipes(self):
        """
        Test listing tags to those assigned to recipes
        """

        in1 = Tag.objects.create(user=self.user, name='Tag99')
        in2 = Tag.objects.create(user=self.user, name='Tag100')
        recipe = Recipe.objects.create(
            title='Recipe 4',
            time_minutes=5,
            price=Decimal('4.50'),
            user=self.user
        )
        recipe.tags.add(in1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        s1 = TagSerializer(in1)
        s2 = TagSerializer(in2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_tags_unique(self):
        """
        Test filtered tags returns a unique list
        """

        ing = Tag.objects.create(user=self.user, name='Tag1')
        Tag.objects.create(user=self.user, name='Tag2')
        recipe1 = Recipe.objects.create(
            title='Recipe 6',
            time_minutes=10,
            price=Decimal('99.10'),
            user=self.user
        )
        recipe2 = Recipe.objects.create(
            title='Recipe 7',
            time_minutes=20,
            price=Decimal('55.99'),
            user=self.user
        )

        recipe1.tags.add(ing)
        recipe2.tags.add(ing)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)