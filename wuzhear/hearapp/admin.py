from django.contrib import admin
from wuzhear.hearapp.models import Venue, Artist, ConcertDate, Setlist, Song

class VenueAdmin(admin.ModelAdmin):
    pass
admin.site.register(Venue, VenueAdmin)

class ArtistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Artist, ArtistAdmin)

class ConcertDateAdmin(admin.ModelAdmin):
    pass
admin.site.register(ConcertDate, ConcertDateAdmin)

class SetlistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Setlist, SetlistAdmin)

class SongAdmin(admin.ModelAdmin):
    pass
admin.site.register(Song, SongAdmin)