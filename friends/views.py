import json

from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from friends.forms import HostForm, FriendFeedbackForm, GuestForm, PlaceForm
from friends.models import Friend, Hobby, Establishment, Host, Arrangement, Guest, FriendRating


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
        'request_enabled': Host.objects.filter(state=False).count() > 0,
        'data': hosts,
        'donate_disabled': donate_disabled,
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
            FriendRating.objects.create(
                rating=form.cleaned_data['rating'],
                feedback=form.cleaned_data['feedback'],
                target_id=kwargs['id'],
                photo=form.files['photo']
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
    interesting_profiles = available_profiles.select_for_update().filter(
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
        friend = form.save(commit=False)
        friend.place_id = request.session['place_id']
        friend.save()
        form.save_m2m()
    else:
        return register_form(request, form)

    return render(
        request,
        'registration_complete.html',

        {'friend': friend, 'main_url': reverse("friends:main")}
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


