from django.test import TestCase
from .models import CategoryPost


class BasicTest(TestCase):

    def test_fields(self):
        category = CategoryPost()
        category.name = 'TestCategory'
        category.save()

        read_record = CategoryPost.objects.get(pk=1)
        self.assertEqual(read_record, category)

    def test_mainapp_common_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/post/create/')
        self.assertEqual(response.status_code, 302)
