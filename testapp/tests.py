from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from testapp.models import Organization, Shop
from django.contrib.auth.models import User


class OrganizationAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        self.organization = Organization.objects.create(
            name="Test organization",
            description="Test description"
        )
        self.shop = Shop.objects.create(
            organization_id=self.organization,
            name="Test shop",
            description="Test description",
            address="Test street",
            index=12345,
            is_deleted=False
        )

        response = self.client.post("/api/token/", {
            "username": "testuser",
            "password": "testpassword"
        })
        self.token = response.data['access'] # получили JWT токен
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_organizations(self):
        response = self.client.get(reverse('organization-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.organization.name)

    def test_download_shops_csv(self):
        response = self.client.get('/api/organizations/1/shops_file/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('text/csv', response['Content-Type'])
        self.assertIn(self.shop.name, response.content.decode())


class ShopAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        self.organization = Organization.objects.create(
            name="Test organization",
            description="Test description"
        )
        self.shop = Shop.objects.create(
            organization_id=self.organization,
            name="Test shop",
            description="Test description",
            address="Test street",
            index=12345,
            is_deleted=False
        )

        response = self.client.post("/api/token/", {
            "username": "testuser",
            "password": "testpassword"
        })
        self.token = response.data['access']  # получили JWT токен
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_shops(self):
        response = self.client.get(reverse('shop-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.shop.name)

    '''
    def test_create_shop(self):
        data = {
            "organization_id_id": self.organization.id,
            "name": "New Shop",
            "description": "New shop",
            "address": "New St",
            "index": 67890,
            "is_deleted": False
        }
        response = self.client.post(reverse('shop-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Shop.objects.filter(name="New Shop").exists())
    '''

    def test_update_shop(self):
        data = {
            "name": "Updated Shop",
            "description": self.shop.description,
            "address": self.shop.address,
            "index": self.shop.index,
            "is_deleted": self.shop.is_deleted
        }
        response = self.client.put(reverse('shop-detail', args=[self.shop.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.shop.refresh_from_db()
        self.assertEqual(self.shop.name, "Updated Shop")

    def test_delete_shop(self):
        response = self.client.delete(reverse('shop-detail', args=[self.shop.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Shop.objects.filter(id=self.shop.id).exists())
