from django.test import TestCase
from .models import CategoryPost, Post

from django.test.client import Client


class BasicTest(TestCase):
    fixtures = ['authapp.json', 'adminapp.json', 'mainapp.json', 'auth.json']

    def test_fields(self):
        category = CategoryPost()
        category.name = 'TestCategory1'
        category.save()

        read_record = CategoryPost.objects.latest('id')
        self.assertEqual(read_record, category)

    def test_mainapp_common_urls(self):

        # Тестируем существование всех страниц статей по категориям
        for category in CategoryPost.objects.all():
            response = self.client.get(f'/category/{category.slug}/')
            self.assertEqual(response.status_code, 200)

        # Тестируем существование всех индивидуальный страниц статей
        for article in Post.objects.all():
            response = self.client.get(f'/post/{article.slug}/')
            self.assertEqual(response.status_code, 200)



