from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from friends.models import Establishment, Friend, Host, Guest, FriendRating, EstablishmentRating, Arrangement


class EstablishmentAdmin(admin.ModelAdmin):
    fields = ['name', 'subjects', 'lat', 'long', 'type']
    list_display = ('name', 'lat', 'long')

admin.site.register(Establishment, EstablishmentAdmin)


class FriendRatingInline(admin.TabularInline):
    model = FriendRating
    extra = 1


class ArrangementInline(admin.StackedInline):
    model = Arrangement


def make_booked(modeladmin, request, queryset):
    queryset.update(state=True)


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    # fields = ['name', 'age', 'place', 'sex']
    list_display = ('html_name', 'age', 'place', 'state', 'partner_sex')
    readonly_fields = ['sex', 'partner_sex']
    search_fields = ['name']
    list_filter = ('sex', 'place', 'state')

    filter_vertical = ['hobbies', ]

    fieldsets = (
        (None, {
            'fields': ('name', 'age', 'sex', 'partner_sex')
        }),
        ('Advanced options', {'fields': ('place', 'hobbies', )}
         )
    )

    @admin.action(description='Mark selected people as active')
    def make_active(self, request, queryset):
        queryset.update(state=False)

    actions = [make_booked, make_active, ]

    @admin.display(description='Name')
    def html_name(self, obj):
        return mark_safe(f'<s>{obj.name}</s>') if obj.state else obj.name

    @admin.display(description='Desired sex')
    def partner_sex(self, obj):
        return 'Male' if obj.sex.lower() == 'f' else 'Female'




class HostAdmin(admin.ModelAdmin):
    fields = ['name', 'age', 'place', 'max_guest_bill', 'hobbies']
    list_display = ('name', 'age', 'place', 'state')

    inlines = [FriendRatingInline, ArrangementInline]

admin.site.register(Host, HostAdmin)


class GuestAdmin(admin.ModelAdmin):
    fields = ['name', 'age', 'place', 'desired_order_value', 'hobbies']
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

