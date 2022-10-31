from django.contrib import admin
from .models import Venue, WebsiteUser, Event

admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(WebsiteUser)