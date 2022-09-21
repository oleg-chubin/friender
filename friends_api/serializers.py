from rest_framework import serializers

from friends.models import Establishment, FriendRating


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = ['name', 'lat', 'long', 'type', 'max_visitors', 'visitor_count']


class FriendRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRating
        exclude = ('photo', )