from django.test import TestCase 
from django.contrib.auth.models import User

# Create your tests here.

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', password='pass123')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('pass123'))

class UserLoginTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='pass123')

    def test_login(self):
        login = self.client.login(username='testuser', password='pass123')
        
        self.assertTrue(login)
        