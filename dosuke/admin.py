from django.contrib import admin
from .models import Item, Event

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass