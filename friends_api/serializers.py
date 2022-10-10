from rest_framework import serializers

from friends.models import Establishment, FriendRating, MenuItem


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        exclude = ('subjects', )


class FriendRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRating
        exclude = ('photo', )


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        exclude = ('place', )
