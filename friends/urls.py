from django.urls import path, re_path

from . import views


app_name = 'friends'
urlpatterns = [
    path('', views.register_form, name='main'),
    path('place', views.place, name='place'),
    path('list', views.list, name='list'),
    path('find_friend', views.find_someone, name='find_friend'),
    re_path('register/(?P<sex>[\w-]+)', views.register, name='register'),
]