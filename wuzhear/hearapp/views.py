# Create your views here.
from django.template import Context, loader
from hearapp.models import Venue, ConcertDate, Setlist
from django.http import HttpResponse
from django.db import models
from django.template.response import TemplateResponse
from datetime import datetime
 
def index(request):
    full_venue_list = Venue.objects.all()
    full_concert_list = ConcertDate.objects.all()
    t = loader.get_template('hearapp/index.html')
    c = Context({
        'full_venue_list': full_venue_list,
    })
    return HttpResponse(t.render(c))

def getConcerts(request, venue_id):
    venue_name = Venue.objects.get(lfm_venue_id=venue_id)
    venue_concert_list = ConcertDate.objects.filter(venue=venue_name)
    t = loader.get_template('hearapp/venueView.html')
    c = Context({
        'venue_concert_list': venue_concert_list,
        'venue_name': venue_name
    })
    return HttpResponse(t.render(c))



def getSetlist(request, concert_id):
    this_concert = Setlist.objects.filter(concerts=concert_id)
    if this_concert:
        concert_songs = this_concert.songs
        official_setlist = this_concert.real_setlist
    else:
        concert_songs = None
        official_setlist = None
    
    t = loader.get_template('hearapp/concertView.html')
    c = Context({
        'concert_id': concert_id,
        'this_concert': this_concert,
        'concert_songs': concert_songs,
        'official_setlist': official_setlist
    })
    return HttpResponse(t.render(c))



    # // concertList=""
    # //  if latest_concert_list
    # //     concertList+="<ul>"
    # //     {% for concert in latest_concert_list %}
    # //         concertList+='<li><button onclick="selectConcert({{ concert.lfm_venue_id }})"/>{{ year }}{{ concert }}</button></li>'
    # //     {% endfor %}
    # //     concertList+="</ul>"
    # // else
    # //     concertList+="<p>No concerts are available.</p>"

    # //  document.getElementById("concertList").innerHTML=concertList;



#     ConcertDate(models.Model):
#     artist = models.ForeignKey(Artist)
#     venue = models.ForeignKey(Venue)