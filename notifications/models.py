from django.db import models

# Create your models here.
from friends.models import Friend


class Notification(models.Model):
    subject = models.TextField()
    text = models.TextField()
    receiver = models.ForeignKey(Friend, on_delete=models.CASCADE)


def place_changed(sender, instance, update_fields, **kwargs):
    instance.age += 23
    if instance.place:
        for friend in instance.place.friend_set.all():
            Notification.objects.create(
                subject='new visitor', text='we have noticed new visitor', receiver=friend
            )

models.signals.pre_save.connect(place_changed, Friend)