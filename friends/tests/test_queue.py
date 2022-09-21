# import os
# import sys
# sys.path.insert(0, os.path.join(__file__, '../../..'))

import unittest

from django.test import TestCase, Client

from friends.models import Guest, Hobby, Host, Pub
from friends.utils import Queue


class TestQueue(TestCase):
    POSSIBLE_STRATEGIES = ['FIFO', 'LIFO']

    def test_queue_initialization(self):
        for strategy in self.POSSIBLE_STRATEGIES:
            queue = Queue(strategy)

    def test_queue_initialization_wrong_argument(self):
        with self.assertRaises(ValueError) as errpr:
            queue = Queue('FIFA')

    def test_fifo_queue_add_value(self):
        for strategy in self.POSSIBLE_STRATEGIES:
            queue = Queue(strategy)
            queue.add(1)

    def test_fifo_queue_pop_value(self):
        first_value = 1
        for strategy in self.POSSIBLE_STRATEGIES:
            queue = Queue(strategy)
            queue.add(first_value)
            value = queue.pop()
            self.assertEqual(value, first_value)

    def test_fifo_queue_pop_value_multivalues(self):
        first_value = 1
        queue = Queue('FIFO')
        queue.add(first_value)
        for i in range(23, 43):
            queue.add(i)
        value = queue.pop()
        self.assertEqual(value, first_value)

    def test_fifo_queue_pop_many_values_multivalues(self):
        values = [1, 23, 1]
        queue = Queue('FIFO')
        for val in values:
            queue.add(val)

        for val in values:
            value = queue.pop()
            self.assertEqual(value, val)

    def test_fifo_queue_pop_repeated_values_multivalues(self):
        values = [1, 1, 23]
        queue = Queue('FIFO')
        for val in values:
            queue.add(val)

        for val in values:
            value = queue.pop()
            self.assertEqual(value, val)

    def test_lifo_queue_pop_repeated_values_multivalues(self):
        values = [1, 1, 23]
        queue = Queue('LIFO')
        for val in values:
            queue.add(val)

        for val in reversed(values):
            value = queue.pop()
            self.assertEqual(value, val)

    def test_queue_pop_emptied_queue(self):
        value = 23
        for strategy in self.POSSIBLE_STRATEGIES:
            queue = Queue(strategy)
            queue.add(value)
            queue.pop()
            with self.assertRaises(ValueError):
                value = queue.pop()


class TestFindSomeoneForm(TestCase):
    def test_success(self):
        guest_name = 'Oleg'
        guest_desired_order_value = 40
        hobby_obj = Hobby.objects.create(name='sport')
        guest_hobbies = [hobby_obj.id]

        client = Client()
        response = client.post(
            '/pals/find_friend',
            {
                'name': guest_name,
                'desired_order_value': guest_desired_order_value,
                'hobbies': guest_hobbies
            }
        )
        self.assertEqual(response.status_code, 200)
        guests = Guest.objects.all()
        self.assertEqual(len(guests), 1)
        guest = guests[0]
        self.assertEqual(guest.name, guest_name)
        self.assertEqual(guest.desired_order_value, guest_desired_order_value)
        self.assertIs(response.context['arrangement'], None)


class TestRegisterForm(TestCase):
    def test_success(self):
        host_name = 'Oleg'
        host_desired_order_value = 40
        hobby_obj = Hobby.objects.create(name='sport')
        Pub.objects.create(name='2323', long=23, lat=-2, max_visitors=10, visitor_count=1)
        host_hobbies = [hobby_obj.id]

        client = Client()
        response = client.post(
            '/pals/register/m',
            {
                'name': host_name,
                'max_guest_bill': host_desired_order_value,
                'sex': 'm',
                'age': 34,
                'hobbies': host_hobbies
            }
        )
        self.assertEqual(response.status_code, 200)
        hosts = Host.objects.all()
        self.assertEqual(len(hosts), 1)
        host = hosts[0]
        self.assertEqual(host.name, host_name)
        self.assertEqual(host.max_guest_bill, host_desired_order_value)
        self.assertIs(response.context['arrangement'], None)

    def test_success_nonempty_queue(self):
        guest = Guest.objects.create(name='Anna', age=23, desired_order_value=12)
        Queue('FIFO').add(guest.id)
        host_name = 'Oleg'
        host_desired_order_value = 40
        hobby_obj = Hobby.objects.create(name='sport')
        Pub.objects.create(name='2323', long=23, lat=-2, max_visitors=10, visitor_count=1)
        host_hobbies = [hobby_obj.id]

        client = Client()
        response = client.post(
            '/pals/register/m',
            {
                'name': host_name,
                'max_guest_bill': host_desired_order_value,
                'sex': 'm',
                'age': 34,
                'hobbies': host_hobbies
            }
        )
        self.assertEqual(response.status_code, 200)
        hosts = Host.objects.all()
        self.assertEqual(len(hosts), 1)
        host = hosts[0]
        self.assertEqual(host.name, host_name)
        self.assertEqual(host.max_guest_bill, host_desired_order_value)
        self.assertIsNotNone(response.context['arrangement'])
        self.assertEqual(response.context['arrangement'].host, host)
        self.assertEqual(response.context['arrangement'].guest, guest)



if __name__ == '__main__':
    unittest.main()
