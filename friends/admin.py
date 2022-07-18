from django.contrib import admin

# Register your models here.
from friends.models import Establishment, Friend, Host, Guest, FriendRating, EstablishmentRating, Arrangement


class EstablishmentAdmin(admin.ModelAdmin):
    fields = ['name', 'subjects', 'lat', 'long', 'type']
    list_display = ('name', 'lat', 'long')

admin.site.register(Establishment, EstablishmentAdmin)


class FriendAdmin(admin.ModelAdmin):
    fields = ['name', 'age', 'place']
    list_display = ('name', 'age', 'place', 'state')

admin.site.register(Friend, FriendAdmin)


class HostAdmin(admin.ModelAdmin):
    fields = ['name', 'age', 'place', 'max_guest_bill']
    list_display = ('name', 'age', 'place', 'state')

admin.site.register(Host, HostAdmin)


class GuestAdmin(admin.ModelAdmin):
    fields = ['name', 'age', 'place', 'desired_order_value']
    list_display = ('name', 'age', 'place', 'state')

admin.site.register(Guest, GuestAdmin)


class FriendRatingAdmin(admin.ModelAdmin):
    fields = ['rating', 'feedback', 'target']
    list_display = ('rating', )

admin.site.register(FriendRating, FriendRatingAdmin)


class EstablishmentRatingAdmin(admin.ModelAdmin):
    fields = ['rating', 'feedback', 'target']
    list_display = ('rating', )

admin.site.register(EstablishmentRating, EstablishmentRatingAdmin)


class ArrangementAdmin(admin.ModelAdmin):
    fields = ['host', 'guest', 'place']
    list_display = ('host', 'guest', 'place')

admin.site.register(Arrangement, ArrangementAdmin)

