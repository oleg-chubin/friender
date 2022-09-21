from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, views
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from friends.models import Establishment, FriendRating

# Create your views here.
from friends_api.authentication import BearerTokenAuthentication
from friends_api.serializers import PlaceSerializer, FriendRatingSerializer



class PlacesAPIView(generics.ListCreateAPIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Establishment.objects.all()
    serializer_class = PlaceSerializer


class PlaceAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Establishment.objects.all()
    serializer_class = PlaceSerializer


class RatingsAPIView(generics.ListCreateAPIView):
    queryset = FriendRating.objects.all()
    serializer_class = FriendRatingSerializer


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, rating_id, format=None):
        file_obj = request.data['file']
        obj = FriendRating.objects.get(pk=rating_id)
        obj.photo = file_obj
        obj.save()
        return Response(status=204)

