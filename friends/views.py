import json
import time
from logging import getLogger
from threading import Thread
from time import sleep

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.transaction import atomic
from django.http import HttpResponse
from django.core.cache import cache, caches

from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.decorators.cache import cache_page, cache_control
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from friends.forms import HostForm, FriendFeedbackForm, GuestForm, PlaceForm, OrderFormset
from friends.models import Friend, Hobby, Establishment, Host, Arrangement, Guest, FriendRating
from friends.tasks import process_image, rotate_image, create_image_if_necessary
from friends.utils import Queue

logger = getLogger(__name__)


def register_form(request, host_form=None, guest_form=None):
    active_hosts = Host.objects.filter(state=False)

    donate_disabled = False
    if request.session.get('place_id'):
        place = Establishment.objects.get(id=request.session['place_id'])
        donate_disabled = not place.has_free_places()

        active_hosts = active_hosts.filter(place_id=request.session['place_id'])

    hosts = active_hosts.select_related('place').prefetch_related('hobbies').order_by('name')[:50]

    context = {
        'find_url': reverse('friends:find_friend'),
        'register_url': reverse("friends:register", kwargs={"sex": "m"}),
        'host_form': host_form if host_form else HostForm(),
        'guest_form': guest_form if guest_form else GuestForm(),
        'request_enabled': True,
        'data': hosts,
        'donate_disabled': donate_disabled,
        # 'foo_value': request.foo_value,
    }
    return render(request, 'form.html', context)


def set_session_place(request):
    form = PlaceForm(data=request.POST)
    if form.is_valid():
        request.session['place_id'] = form.cleaned_data['place'].id
    return redirect('friends:main')


def share_friend_feedback(request, **kwargs):
    context = {}
    if request.method == 'POST':
        form = FriendFeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            friend_rating = FriendRating(
                rating=form.cleaned_data['rating'],
                feedback=form.cleaned_data['feedback'],
                target_id=kwargs['id'])
            if 'photo' in form.files:
                friend_rating.photo = form.files['photo']
            friend_rating.save()

            tasks = create_image_if_necessary.s(friend_rating.id) #| process_image.s() | rotate_image.s()
            tasks()
            return redirect('friends:list')
        context['form'] = form
    else:
        context['form'] = FriendFeedbackForm()
    return render(request, 'friend_feedback_form.html', context)


# @cache_page(60, cache='userlist')
# @cache_control(public=True)
def list(request):
    data = cache.get('some_var')
    context = {'profiles': Friend.objects.all().prefetch_related('friendrating_set')}
    return render(request, 'list.html', context)

def place(request, id=None):
    context = {'places': Establishment.objects.prefetch_related('friend_set__hobbies').all()[:3]}
    return render(request, 'place.html', context)


@transaction.atomic
def find_someone(request):
    form = GuestForm(request.POST)

    if not form.is_valid():
        return register_form(request, guest_form=form)

    guest = form.save(commit=False)
    guest.age = 23
    guest.save()
    form.save_m2m()

    available_profiles = Host.objects.filter(state=False)
    ordered_profiles = available_profiles.order_by('id')
    interesting_profiles = ordered_profiles.select_for_update().filter(
        hobbies__in=form.cleaned_data['hobbies']
    )
    interesting_profiles = interesting_profiles.filter(
        max_guest_bill__gte=form.cleaned_data['desired_order_value']
    )

    profile = interesting_profiles.first()
    arrangement = None
    if profile:
        arrangement = make_arrangement(guest, profile)
        return redirect('friends:preorder', arrangement_id=arrangement.id)

    queue = Queue(Queue.FIFO)
    queue.add(guest.id)
    return redirect('friends:main')





def make_arrangement(guest, profile):
    profile.state = True
    profile.save()
    default_place = Establishment.objects.order_by('?')[0]
    arrangement = Arrangement.objects.create(
        host=profile, guest=guest, place=profile.place or default_place
    )
    return arrangement


def long_time_task():
    # time.sleep(10)
    logger.debug('I am done')


@transaction.atomic
def register(request, sex=None):
    form = HostForm(request.POST)

    if form.is_valid():
        friend = form.save(commit=False)
        friend.place_id = request.session.get('place_id', Establishment.objects.first().id)
        friend.save()
        form.save_m2m()
    else:
        return register_form(request, form)

    queue = Queue(Queue.FIFO)
    guest = queue.pop()
    if guest:
        guest = Guest.objects.get(id=guest)
        arrangement = make_arrangement(guest, friend)
    else:
        arrangement = None

    return render(
        request,
        'registration_complete.html',

        {
            'friend': friend,
            'main_url': reverse("friends:main"),
            'arrangement': arrangement,
        }
    )


class PlacesView(ListView):
    template_name = "places_list.html"
    model = Establishment
    context_object_name = 'places'

    paginate_by = 3


class PlaceSerializerMixin:
    def serialize(self, place):
        return {"id": place.id, "name": place.name, "latitude": place.lat, "longitude": place.long}


class PlacesApiView(BaseListView, PlaceSerializerMixin):
    model = Establishment
    context_object_name = 'places'
    paginate_by = 3

    def render_to_response(self, context):
        data = [self.serialize(place) for place in context['places']]
        body = json.dumps(data)
        return HttpResponse(body, content_type='application/json', status=200)


class PlaceApiDetailView(BaseDetailView, PlaceSerializerMixin):
    model = Establishment
    context_object_name = 'place'

    def render_to_response(self, context):
        data = self.serialize(context['place'])
        body = json.dumps(data)
        return HttpResponse(body, content_type='application/json', status=200)


class CreatePlaceView(CreateView):
    template_name = "create.html"
    model = Establishment
    fields = ('name', 'lat', 'long', 'type')
    success_url = reverse_lazy('friends:places')


def make_preorder(request, arrangement_id):
    arrangement = Arrangement.objects.get(id=arrangement_id)
    if request.method == 'POST':
        formset = OrderFormset(
            instance=arrangement,
            data=request.POST,
            files=request.FILES
        )
        if formset.is_valid():
            formset.save()
            return redirect('friends:main')
    else:
        formset = OrderFormset(instance=arrangement)
    return render(request, 'preorder.html', {'formset': formset})