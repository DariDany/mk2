# books/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import Recipe
from django.utils import timezone

class RecipeViewsTest(TestCase):
    def setUp(self):
        self.recipe1 = Recipe.objects.create(
            name='Recipe 1',
            description='Description 1',
            created_at=timezone.now()
        )
        self.recipe2 = Recipe.objects.create(
            name='Recipe 2',
            description='Description 2',
            created_at=timezone.now().replace(year=2023)
        )

    def test_main_view(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertContains(response, 'Recipe 2')
        self.assertNotContains(response, 'Recipe 1')

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipe_detail', args=[self.recipe2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_detail.html')
        self.assertContains(response, 'Recipe 2')
        self.assertContains(response, 'Description 2')
