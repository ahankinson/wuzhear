from django.db import models

# Create your models here.
class Venue(models.Model):
    lat = models.CharField(max_length=255)
    lon = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    lfm_venue_id = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class ConcertDate(models.Model):
    artist = models.ForeignKey(Artist)
    venue = models.ForeignKey(Venue)
    date = models.DateField()
    cancelled = models.BooleanField()
    lfm_concert_id = models.CharField(max_length=255)

    def __unicode__(self):
        return self.venue.name

class Song(models.Model):
    song_name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist)
    en_id = models.CharField(max_length=255)

    def __unicode__(self):
        return self.song_name

class Setlist(models.Model):
    concerts = models.ForeignKey(ConcertDate)
    songs = models.ManyToManyField(Song)
    real_setlist = models.BooleanField()