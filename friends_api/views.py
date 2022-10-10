from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, views, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from friends.models import Establishment, FriendRating, MenuItem

# Create your views here.
from friends_api.authentication import BearerTokenAuthentication
from friends_api.serializers import PlaceSerializer, FriendRatingSerializer, MenuItemSerializer


class PlacesAPIView(generics.ListCreateAPIView):
    # authentication_classes = [BearerTokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = Establishment.objects.all()
    serializer_class = PlaceSerializer


class PlaceAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Establishment.objects.all()
    serializer_class = PlaceSerializer


class RatingsAPIView(generics.ListCreateAPIView):
    queryset = FriendRating.objects.all()
    serializer_class = FriendRatingSerializer


class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return super().get_queryset().filter(place_id=self.kwargs['place_id'])

    def perform_create(self, serializer):
        serializer.save(place_id=self.kwargs['place_id'])


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, rating_id, format=None):
        file_obj = request.data['file']
        obj = FriendRating.objects.get(pk=rating_id)
        obj.photo = file_obj
        obj.save()
        return Response(status=204)

