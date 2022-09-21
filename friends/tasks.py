# Create your tasks here

# from demoapp.models import Widget
import base64
import time
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files import File
from django.core.files.base import ContentFile

from friends.models import FriendRating

logger = get_task_logger(__name__)


@shared_task(autoretry_for=(FriendRating.DoesNotExist,))
def rotate_image(friend_rating_id):
    friend_rating = FriendRating.objects.get(pk=friend_rating_id)
    image = friend_rating.photo
    img = Image.open(image)
    img = img.rotate(45)
    in_memory_file = BytesIO()
    img.save(in_memory_file, "png")
    friend_rating.photo = ContentFile(in_memory_file.getvalue(), name='hello-world.png')
    friend_rating.save()
    return friend_rating_id


@shared_task(autoretry_for=(FriendRating.DoesNotExist,))
def process_image(friend_rating_id):
    friend_rating = FriendRating.objects.get(pk=friend_rating_id)
    image = friend_rating.photo
    img = Image.open(image)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 50)
    # add watermark
    draw.text((0, 0), "puppy",
              (0, 0, 0), font=font)
    image.seek(0)

    in_memory_file = BytesIO()
    img.save(in_memory_file, "png")
    friend_rating.photo = ContentFile(in_memory_file.getvalue(), name='hello-world.png')
    friend_rating.save()
    return friend_rating_id


@shared_task(autoretry_for=(FriendRating.DoesNotExist,))
def create_image_if_necessary(friend_rating_id):
    friend_rating = FriendRating.objects.get(pk=friend_rating_id)
    if not friend_rating.photo:
        response = requests.post(
            'https://bf.dallemini.ai/generate',
            json={'prompt': friend_rating.feedback}
        )
        data = base64.b64decode(response.json()['images'][0])
        # img = Image.new('RGB', (200, 200), color='red')
        # draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype("arial.ttf", 50)
        # # add watermark
        # draw.text((0, 0), "puppy",
        #           (0, 0, 0), font=font)

        # in_memory_file = BytesIO()
        # img.save(in_memory_file, "png")
        friend_rating.photo = ContentFile(data, name='hello-world.png')
        friend_rating.save()
    return friend_rating.id


@shared_task
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return (x + y)*2