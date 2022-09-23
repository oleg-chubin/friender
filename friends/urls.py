from django.urls import path, re_path

from . import views


app_name = 'friends'
urlpatterns = [
    path('', views.register_form, name='main'),
    re_path('arrangement/preorder/(?P<arrangement_id>[\d-]+)', views.make_preorder, name='preorder'),
    path('api/places', views.PlacesApiView.as_view(), name='places_api'),
    path('set_place', views.set_session_place, name='set_session_place'),
    re_path('api/places/(?P<pk>[\d-]+)', views.PlaceApiDetailView.as_view(), name='place_api'),
    path('places/create', views.CreatePlaceView.as_view(), name='places_create'),
    path('places', views.PlacesView.as_view(), name='places'),
    path('place', views.place, name='place'),
    path('list', views.list, name='list'),
    re_path('friend/(?P<id>[\d-]+)/feedback', views.share_friend_feedback, name='friend_feedback'),
    path('find_friend', views.find_someone, name='find_friend'),
    re_path('register/(?P<sex>[\w-]+)', views.register, name='register'),
]