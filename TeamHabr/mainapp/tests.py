from django.test import TestCase
from .models import CategoryPost


class BasicTest(TestCase):
    # fixtures = ['mainapp.json']

    def test_fields(self):
        category = CategoryPost()
        category.name = 'TestCategory1'
        category.save()

        read_record = CategoryPost.objects.get(pk=1)
        self.assertEqual(read_record, category)

    def test_mainapp_common_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/post_list.html')
        self.assertTrue(response.context['user'].is_anonymous)

        response = self.client.get('/post/create/')
        self.assertEqual(response.status_code, 302)


