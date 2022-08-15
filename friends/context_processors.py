from friends.forms import PlaceForm
from friends.models import Establishment, Pub


def post_form(request):
    return {
        'place_form': PlaceForm(data={'place': request.session.get('place_id', None)}),
        'places': Pub.objects.get_available_pubs()
    }
