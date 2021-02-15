from django.test import TestCase
from .models import User



class BasicTest(TestCase):
    fixtures = ['authapp.json', 'auth.json']

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'testuser@mail.com', 'testpassword')

    def test_user_creation(self):

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/post_list.html')
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Выход', status_code=200)

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/account/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser', status_code=200)
        self.assertContains(response, 'testuser@mail.com', status_code=200)
        self.assertContains(response, 'Выход', status_code=200)


