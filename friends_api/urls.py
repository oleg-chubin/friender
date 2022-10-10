from django.urls import path, re_path

from friends_api.views import FileUploadView
from . import views



app_name = 'friends_api'
urlpatterns = [
    path('places', views.PlacesAPIView.as_view()),
    re_path('places/(?P<pk>[\d-]+)$', views.PlaceAPIView.as_view()),
    re_path('places/(?P<place_id>[\d-]+)/menu$', views.MenuItemView.as_view()),
    path('ratings', views.RatingsAPIView.as_view()),
    re_path(r'^ratings/(?P<rating_id>[\d-]+)/photo$', FileUploadView.as_view())
]