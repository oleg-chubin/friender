import json

from django.http import HttpResponse
from django.urls import reverse
from django.db import transaction
from django.shortcuts import render, redirect

from friends.forms import HostForm, FriendFeedbackForm, GuestForm
from friends.models import Friend, Hobby, Establishment, Host, Arrangement, Guest, FriendRating


def register_form(request, host_form=None, guest_form=None):
    context = {
        'find_url': reverse('friends:find_friend'),
        'register_url': reverse("friends:register", kwargs={"sex": "m"}),
        'host_form': host_form if host_form else HostForm(),
        'guest_form': guest_form if guest_form else GuestForm(),
        'data': Host.objects.filter(state=False).select_related('place').prefetch_related('hobbies').order_by('name')[:50]
    }
    return render(request, 'form.html', context)


def share_friend_feedback(request, **kwargs):
    context = {}
    if request.method == 'POST':
        form = FriendFeedbackForm(request.POST)
        if form.is_valid():
            FriendRating.objects.create(
                rating=form.cleaned_data['rating'],
                feedback=form.cleaned_data['feedback'],
                target_id=kwargs['id']
            )
            return redirect('friends:list')
        context['form'] = form
    else:
        context['form'] = FriendFeedbackForm()
    return render(request, 'friend_feedback_form.html', context)


def list(request):
    context = {'profiles': Friend.objects.all().prefetch_related('friendrating_set')}
    return render(request, 'list.html', context)

def place(request, id=None):
    context = {'places': Establishment.objects.prefetch_related('friend_set__hobbies').all()[:3]}
    return render(request, 'place.html', context)


@transaction.atomic
def find_someone(request):
    form = GuestForm(request.POST)

    if not form.is_valid():
        return register_form(guest_form=form)

    guest = form.save(commit=False)
    guest.age = 23
    guest.save()
    form.save_m2m()

    available_profiles = Host.objects.order_by('id').filter(state=False)
    interesting_profiles = available_profiles.filter(
        hobbies__in=form.cleaned_data['hobbies'],
        max_guest_bill__gte=form.cleaned_data['desired_order_value']
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
    form = HostForm(request.POST)
    if form.is_valid():
        friend = form.save()
    else:
        return register_form(request, form)

    return render(
        request,
        'registration_complete.html',

        {'friend': friend, 'main_url': reverse("friends:main")}
    )


