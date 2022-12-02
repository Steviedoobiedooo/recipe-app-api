"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class ModelTests(TestCase):
    """
    Test models
    """

    def test_create_user_with_email_successful(self):
        """
        Test creating a user with an email is successful
        """

        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """
        Test if email is normalized for new users
        """

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email)
            self.assertEqual(user.email, expected)


    def test_new_user_without_email_raises_error(self):
        """
        Test that creating a user without email raises a ValueError
        """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')


    def test_create_superuser(self):
        """
        Test creating a superuser
        """

        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


    def test_edit_user_page(self):
        """
        Test the edit user page
        """

        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)