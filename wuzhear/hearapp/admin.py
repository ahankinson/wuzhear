from django.contrib import admin
from wuzhear.hearapp.models import Venue, Artist, ConcertDate, Setlist, Song

class VenueAdmin(admin.ModelAdmin):
    pass
admin.site.register(Venue, VenueAdmin)

class ArtistAdmin(admin.ModelAdmin):
    search_fields = ("name",)
admin.site.register(Artist, ArtistAdmin)

class ConcertDateAdmin(admin.ModelAdmin):
    list_display = ("venue", "artist", "date")
    search_fields = ("artist",)
admin.site.register(ConcertDate, ConcertDateAdmin)

class SetlistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Setlist, SetlistAdmin)

class SongAdmin(admin.ModelAdmin):
    pass
admin.site.register(Song, SongAdmin)