import json

from django.http import HttpResponse
from django.urls import reverse
from django.db import transaction
from django.shortcuts import render

from friends.models import Friend, Hobby, Establishment, Host, Arrangement, Guest


def register_form(request):
    context = {
        'find_url': reverse('friends:find_friend'),
        'register_url': reverse("friends:register", kwargs={"sex": "m"}),
        'data': Host.objects.filter(state=False).select_related('place').prefetch_related('hobbies').order_by('name')[:50]
    }
    return render(request, 'form.html', context)


def list(request):
    context = {'profiles': Friend.objects.all()}
    return render(request, 'list.html', context)

def place(request, id=None):
    context = {'places': Establishment.objects.prefetch_related('friend_set__hobbies').all()[:3]}
    return render(request, 'place.html', context)


@transaction.atomic
def find_someone(request):
    hobbies = [i.strip().lower() for i in request.POST['hobby'].split(',')]
    desired_bill = request.POST['desired_bill_value']
    name = request.POST['name']

    available_profiles = Host.objects.order_by('id').filter(state=False)
    interesting_profiles = available_profiles.filter(
        hobbies__name__in=hobbies,
        max_guest_bill__gte=desired_bill
    )
    guest = Guest.objects.create(
        name=name,
        age=23,
        desired_order_value=int(desired_bill)
    )
    profile = interesting_profiles.first()
    arrangement = None
    if profile:
        profile.state = True
        profile.save()

        default_place = Establishment.objects.order_by('?')[0]

        arrangement = Arrangement.objects.create(
           host=profile, guest=guest, place=profile.place or default_place
        )

    return render(request, 'search_complete.html', {'arrangement': arrangement})


def register(request, sex=None):
    name = request.POST['name']
    friend = Host.objects.create(
        name=name,
        age=int(request.POST['age']),
        max_guest_bill=int(request.POST['max_bill_value']),
        sex=sex
    )
    hobbies = [i.strip().lower() for i in request.POST['hobby'].split(',')]
    hobby_objects = []
    for hobby in hobbies:
        hobby_obj, _ = Hobby.objects.get_or_create(name=hobby)
        hobby_objects.append(hobby_obj)

    friend.hobbies.add(*hobby_objects)

    return render(
        request,
        'registration_complete.html',

        {'friend': friend, 'main_url': reverse("friends:main")}
    )


