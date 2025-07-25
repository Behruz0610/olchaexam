
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Product, Comment

User = get_user_model()


from rest_framework.test import force_authenticate

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='TestCat')
        self.product = Product.objects.create(name='TestProduct', category=self.category, price=10, description='desc')
        # JWT token olish
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username': 'testuser', 'password': 'testpass'})
        self.token = resp.data['access']
        self.auth = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url, **self.auth)
        self.assertEqual(response.status_code, 200)

    def test_product_create_auth(self):
        url = reverse('product-list')
        data = {'name': 'NewProduct', 'category_id': self.category.id, 'price': 20, 'description': 'desc'}
        response = self.client.post(url, data, **self.auth)
        self.assertEqual(response.status_code, 201)

class CommentAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='TestCat')
        self.product = Product.objects.create(name='TestProduct', category=self.category, price=10, description='desc')
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username': 'testuser', 'password': 'testpass'})
        self.token = resp.data['access']
        self.auth = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

    def test_comment_create(self):
        url = reverse('comment-list')
        data = {'product': self.product.id, 'content': 'Test comment'}
        response = self.client.post(url, data, **self.auth)
        self.assertEqual(response.status_code, 201)
