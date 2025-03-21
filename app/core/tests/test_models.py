"""
Tests for models
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """ Test Models """
    def test_create_user_with_email_successful(self):
        """ Test creating a user with an email is successful """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test the email for a new user is normalized """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Test creating user with no email raises a ValueError """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser_successful(self):
        """ Test creating a superuser """
        superuser = get_user_model().objects.create_superuser(
            'admin@example.com',
            'adminpass123'
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_recipe(self):
        """ Test creating a recipe is successful """
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description'
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """ Test creating a tag is successful """
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        tag = models.Tag.objects.create(user=user, name='Tag name')
        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """ Test creating an ingredient is successful """
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient name'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """ Test that image is saved in the correct location """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
