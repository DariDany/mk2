# books/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import Category, Recipe
from django.utils import timezone


class RecipeViewsTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
            name='Dessert')  # Create a category instance
        self.recipe1 = Recipe.objects.create(
            title='Recipe 1',
            description='Description 1',
            created_at=timezone.now(),
            category=category  # Assign the category to the recipe
        )
        self.recipe2 = Recipe.objects.create(
            title='Recipe 2',
            description='Description 2',
            created_at=timezone.now().replace(year=2023),
            category=category  # Assign the same category to the recipe
        )

    def test_main_view(self):
        response = self.client.get(reverse('main'))
        print(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertNotContains(response, 'Recipe 1')

    def test_recipe_detail_view(self):
        response = self.client.get(
            reverse('recipe_detail', args=[self.recipe2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_detail.html')
        self.assertContains(response, 'Description 2')


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Vegetarian')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = category.name
        self.assertEqual(expected_object_name, str(category))


class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Dessert')
        Recipe.objects.create(
            title='Chocolate Cake',
            description='Delicious chocolate cake recipe',
            instructions='1. Preheat the oven...',
            ingredients='Flour, sugar, cocoa powder...',
            created_at=timezone.now(),
            category=category
        )

    def test_title_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_title(self):
        recipe = Recipe.objects.get(id=1)
        expected_object_name = recipe.title
        self.assertEqual(expected_object_name, str(recipe))

    def test_recipe_category(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.category.name, 'Dessert')
