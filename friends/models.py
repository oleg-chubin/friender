from django.db import models
from django.db.models import Index, F
from django.db.models.functions import Lower


class PubManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Pub')


class RestaurantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Restaurant')


class Hobby(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Establishment(models.Model):
    #name, age, sex
    name = models.CharField(max_length=100)
    lat = models.FloatField(db_column='latitude')
    long = models.FloatField(db_column='longitude')
    subjects = models.ManyToManyField(Hobby)
    type = models.CharField(max_length=16, choices=[('Pub', 'Pub'), ('Restaurant', 'Restaurant')])

    def __str__(self):
        return f'{self.type} {self.name}({self.lat}, {self.long})'


class Pub(Establishment):
    class Meta:
        proxy = True

    objects = PubManager()


class Restaurant(Establishment):
    class Meta:
        proxy = True

    objects = RestaurantManager()


def subjects_hobby_updater(sender, instance, action, **kwargs):
    if action != 'post_add':
        return
    subjects = instance.subjects.all()
    if subjects:
        for friend in instance.friend_set.all():
            for subj in subjects:
                friend.hobbies.add(subj)

models.signals.m2m_changed.connect(receiver=subjects_hobby_updater, sender=Establishment.subjects.through)


class Friend(models.Model):
    #name, age, sex
    POSSIBLE_GENDER = (('m', 'male'), ('f', 'female'))
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    state = models.BooleanField(
        choices=((0, 'Active'), (1, 'Booked')), default=0
    )
    sex = models.CharField(choices=POSSIBLE_GENDER, max_length=2)
    place = models.ForeignKey(Establishment, on_delete=models.CASCADE, null=True)
    hobbies = models.ManyToManyField(Hobby)

    class Meta:
        indexes = [
            Index(Lower('name').asc(), 'age', name='lower_name_age_idx'),
            Index(F('age') * 365, name='age_in_days_idx'),
        ]
        index_together = [['age', 'place']]

    def __str__(self):
        return f'{self.name}({self.age} y.o.)'


class Host(Friend):
    max_guest_bill = models.IntegerField()


class Guest(Friend):
    desired_order_value = models.IntegerField()


class Arrangement(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    place = models.ForeignKey(Establishment, on_delete=models.CASCADE)


class Rating(models.Model):
    rating = models.IntegerField()
    feedback = models.TextField()

    class Meta:
        abstract = True


class EstablishmentRating(Rating):
    target = models.ForeignKey(Establishment, on_delete=models.CASCADE)


class FriendRating(Rating):
    target = models.ForeignKey(Friend, on_delete=models.CASCADE)


def hobby_updater(sender, instance, **kwargs):
    if instance.place:
        for hobby in instance.place.subjects.all():
            instance.hobbies.add(hobby)

models.signals.pre_save.connect(receiver=hobby_updater, sender=Friend)