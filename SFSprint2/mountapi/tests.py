from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, MountainPass, Image
from datetime import datetime
from .managers import *

class MountainPassManagerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', phone='1234567890', name='John', fam='Doe', otc='Smith')

    def test_submit_data(self):
        data = {
            'beauty_title': 'Test Pass',
            'title': 'Test Title',
            'other_titles': 'Test Other Titles',
            'connect': 'Test Connect',
            'add_time': datetime.now().isoformat(),
            'user': self.user.id,
            'coords': {'latitude': '12.345', 'longitude': '67.890', 'height': '1000'},
            'level': {'winter': 'Difficult', 'summer': 'Easy', 'autumn': 'Moderate', 'spring': 'Moderate'},
            'images': [{'data': 'image_data_1', 'title': 'Image 1'}, {'data': 'image_data_2', 'title': 'Image 2'}],
        }

        response = MountainPassManager.submit_data(data, self.user.id)

        self.assertEqual(response['status'], 200)
        self.assertEqual(response['message'], 'Отправлено успешно')
        self.assertIsNotNone(response['id'])

        mountain_pass = MountainPass.objects.get(pk=response['id'])
        self.assertEqual(mountain_pass.beauty_title, 'Test Pass')
        self.assertEqual(mountain_pass.images.count(), 2)

        image_titles = mountain_pass.images.values_list('title', flat=True)
        self.assertIn('Image 1', image_titles)
        self.assertIn('Image 2', image_titles)

class MountainPassAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', phone='1234567890', name='John', fam='Doe', otc='Smith')
        self.mountain_pass = MountainPass.objects.create(
            beauty_title='Test Pass',
            title='Test Title',
            other_titles='Test Other Titles',
            connect='Test Connect',
            add_time=datetime.now(),
            user=self.user,
            coord={'latitude': '12.345', 'longitude': '67.890', 'height': '1000'},
            level={'winter': 'Difficult', 'summer': 'Easy', 'autumn': 'Moderate', 'spring': 'Moderate'},
        )
        self.image_1 = Image.objects.create(mountain_pass=self.mountain_pass, data='image_data_1', title='Image 1')
        self.image_2 = Image.objects.create(mountain_pass=self.mountain_pass, data='image_data_2', title='Image 2')

    def test_get_mountain_pass(self):
        response = self.client.get(reverse('get_mountain_pass', args=[self.mountain_pass.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['beauty_title'], 'Test Pass')
        self.assertEqual(len(response.data['images']), 2)

    def test_edit_mountain_pass(self):
        edited_data = {
            'beauty_title': 'Edited Test Pass',
            'title': 'Edited Test Title',
            'connect': 'Edited Test Connect',
            'coord': {'latitude': '12.345', 'longitude': '67.890', 'height': '1200'},
            'level': {'winter': 'Difficult', 'summer': 'Moderate', 'autumn': 'Moderate', 'spring': 'Moderate'},
        }

        response = self.client.patch(reverse('edit_mountain_pass', args=[self.mountain_pass.id]), data=edited_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 1)

        self.mountain_pass.refresh_from_db()
        self.assertEqual(self.mountain_pass.beauty_title, 'Edited Test Pass')
        self.assertEqual(self.mountain_pass.coord['height'], '1200')
        self.assertEqual(self.mountain_pass.level['summer'], 'Moderate')

    def test_get_user_mountain_pass_list(self):
        response = self.client.get(reverse('get_user_mountain_pass_list'), {'user__email': self.user.email})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['beauty_title'], 'Test Pass')
