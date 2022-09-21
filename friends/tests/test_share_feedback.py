import unittest
from base64 import b64encode
from unittest.mock import patch, MagicMock

from django.test import TestCase, Client, override_settings
from django.urls import reverse

from friends import models

from friends.models import Guest, Hobby, Host, Pub, FriendRating
from friends.utils import Queue


class TestShareFeedback(TestCase):
    def setUp(self):
        self.client = Client()
        self.friend = models.Friend.objects.create(name='Oleg', age=23)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    @patch('friends.tasks.requests')
    def test_success(self, fake_requests):
        img_content = b'1234567890'
        fake_response = MagicMock()
        fake_requests.post.return_value = fake_response
        fake_response.json.return_value = {'images': [b64encode(img_content)]}

        url = reverse('friends:friend_feedback', kwargs={'id': self.friend.id})
        rating_value = 4
        feedback_text = 'some text about a friend'
        response = self.client.post(
            url,
            data={'rating': rating_value, 'feedback': feedback_text})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/pals/list')

        rating = FriendRating.objects.first()
        self.assertEqual(rating.rating, rating_value)
        self.assertEqual(rating.feedback, feedback_text)
        self.assertEqual(rating.target_id, self.friend.id)
        self.assertIsNotNone(rating.photo.url)
        self.assertEqual(rating.photo.read(), img_content)
