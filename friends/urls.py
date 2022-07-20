from django.urls import path, re_path

from . import views


app_name = 'friends'
urlpatterns = [
    path('', views.register_form, name='main'),
    path('place', views.place, name='place'),
    path('list', views.list, name='list'),
    re_path('friend/(?P<id>[\d-]+)/feedback', views.share_friend_feedback, name='friend_feedback'),
    path('find_friend', views.find_someone, name='find_friend'),
    re_path('register/(?P<sex>[\w-]+)', views.register, name='register'),
]