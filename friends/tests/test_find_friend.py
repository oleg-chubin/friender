import threading
import unittest
from base64 import b64encode
from time import sleep
from unittest.mock import patch, MagicMock

from django.test import TransactionTestCase, Client, override_settings
from django.urls import reverse

from friends import models, views

from friends.models import Guest, Hobby, Host, Pub, FriendRating
from friends.utils import Queue


class TestFindHost(TransactionTestCase):
    max_bill = 200

    def setUp(self):
        self.client = Client()
        self.hobby = models.Hobby.objects.create(name='bookscrapping')
        self.host = models.Host.objects.create(
            name='Oleg',
            age=23,
            max_guest_bill=self.max_bill
        )
        self.host.hobbies.add(self.hobby)
        self.pub = models.Pub.objects.create(
            name='pub', lat=12, long=32, max_visitors=100, visitor_count=0
        )
        # self.first_guest = models.Guest.objects.create(
        #     name='Hanna', age=25, desired_order_value=self.max_bill - 10
        # )
        # self.first_guest.hobbies.add(self.hobby)

    def tearDown(self):
        self.hobby.delete()
        self.host.delete()
        self.pub.delete()
        # self.first_guest.delete()

    def make_request(self, name):
        url = reverse('friends:find_friend')
        response = self.client.post(
            url,
            data={
                'name': name,
                'desired_order_value': self.max_bill - 10,
                'hobbies': [self.hobby.id]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_success(self):
        original_make_arrangement = views.make_arrangement
        event = threading.Event()

        def new_behavior(*args, **kw):
            event.wait(timeout=5)
            return original_make_arrangement(*args, **kw)

        with patch('friends.views.make_arrangement') as fake_make_arrangement:
            fake_make_arrangement.side_effect = new_behavior
            thread_hanna = threading.Thread(target=self.make_request, args=('Hanna', ))
            thread_irina = threading.Thread(target=self.make_request, args=('Irina', ))
            thread_hanna.start()
            thread_irina.start()

            sleep(1)
            event.set()

            thread_hanna.join(timeout=5)
            thread_irina.join(timeout=5)

        self.assertEqual(models.Arrangement.objects.count(), 1)
