from django.contrib import admin
from .models import PlanetariumDome, ShowTheme, AstronomyShow, Reservation, ShowSession, Ticket
from django.utils.html import format_html


@admin.register(PlanetariumDome)
class PlanetariumDomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'rows', 'seats_in_row', 'capacity')


@admin.register(ShowTheme)
class ShowThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AstronomyShow)
class AstronomyShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'show_theme_list')

    def show_theme_list(self, obj):
        return ", ".join([theme.name for theme in obj.show_theme.all()])
    show_theme_list.short_description = "Show Themes"


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user')
    inlines = (TicketInline, )


@admin.register(ShowSession)
class ShowSessionAdmin(admin.ModelAdmin):
    list_display = ('astronomy_show', 'planetarium_dome', 'show_time', 'tickets_available')

    def tickets_available(self, obj):
        return obj.tickets_available
    tickets_available.short_description = "Available Tickets"


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('show_session', 'row', 'seat', 'reservation')

