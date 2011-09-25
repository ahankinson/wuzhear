import os
import logging
import pylast
import types
from optparse import OptionParser
import urllib2
import json
import codecs
from datetime import datetime
import pdb


import settings
from django.core.management import setup_environ
project_directory = setup_environ(settings)
project_name = os.path.basename(project_directory)
os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % project_name

from wuzhear.hearapp.models import Artist, ConcertDate, Setlist, Song, Venue

LFM_API_KEY = "6dd5675d77c4eecf6f3334be113b1f1f"
LFM_SECRET = "33b065b56d8c085d04ad76bd3ce8adf7"


def get_venues():
    # r = urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?method=geo.getevents&location=montreal&api_key={0}&format=json&limit=317".format(LFM_API_KEY))
    # print dir(r)
    # raw_input()
    # f = open('lfmdata/georesults.txt', 'w')
    # f.write(r.read())
    # f.close()
    f = codecs.open("../lfmdata/georesults.txt", 'r', 'utf-8')
    contents = f.read()
    f.close()
    results = json.loads(contents)
    events = results['events']['event']
    ven = {}
    for event in events:
        venue = event['venue']
        vid = venue['id']
        vname = venue['name']
        ven[vid] = {}
        ven[vid]['name'] = vname
        ven[vid]['lat'] = venue['location']['geo:point']['geo:lat']
        ven[vid]['lon'] = venue['location']['geo:point']['geo:long']
    return ven

def add_venues_to_database(venues):
    for venue_id, venue_info in venues.iteritems():
        v = Venue(name=venue_info['name'], lfm_venue_id=venue_id, lat=venue_info['lat'], lon=venue_info['lon'])
        v.save()


def get_concerts_for_venue(venue_id):
    lg.debug(venue_id)
    # r = urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?method=venue.getpastevents&api_key={0}&venue={1}&limit=1000&format=json".format(LFM_API_KEY, venue_id))
    # f = codecs.open("lfmdata/{0}.txt".format(venue_id), 'w', 'utf-8')
    # content = unicode(r.read(), errors = "ignore")
    # f.write(content)
    # f.close()
    f = codecs.open("../lfmdata/{0}.txt".format(venue_id), 'r', 'utf-8')
    contents = f.read()
    f.close()
    results = json.loads(contents)
    # lg.debug(results)

    # pdb.set_trace()
    if "event" not in results['events'].keys():
        total = results['events']['total']
    else:
        total = results['events']['@attr']['total']

    if int(total) == 0:
        print "No events found for {0}".format(venue_id)
        return

    events = results['events']['event']

    if isinstance(events, types.ListType):
        for event in events:
            lfm_concert_id = event['id']
            artists = event['artists']['artist']
            start_date = event['startDate']
            cancelled = event['cancelled']
            venue = event['venue']['id']
            if isinstance(artists, types.ListType):
                for artist in artists:
                    a, created = Artist.objects.get_or_create(name=artist)
                    if created:
                        a.save()
                    v = Venue.objects.get(lfm_venue_id=venue)
                    cdate = datetime.strptime(start_date, "%a, %d %b %Y %H:%M:%S")
                    if int(cancelled) != 0:
                        cancelled = True
                    else:
                        cancelled = False

                    c = ConcertDate(artist = a, venue = v, date = cdate, cancelled=cancelled, lfm_concert_id=lfm_concert_id)
                    c.save()
            else:
                # make a new concert for every artist
                a, created = Artist.objects.get_or_create(name=artists)
                if created:
                    a.save()
                v = Venue.objects.get(lfm_venue_id=venue)
                cdate = datetime.strptime(start_date, "%a, %d %b %Y %H:%M:%S")
                if int(cancelled) != 0:
                    cancelled = True
                else:
                    cancelled = False
                    
                c = ConcertDate(artist = a, venue = v, date = cdate, cancelled=cancelled, lfm_concert_id=lfm_concert_id)
                c.save()
    else:
        lfm_concert_id = events['id']
        artists = events['artists']['artist']
        start_date = events['startDate']
        cancelled = events['cancelled']
        venue = events['venue']['id']
        if isinstance(artists, types.ListType):
            for artist in artists:
                a, created = Artist.objects.get_or_create(name=artist)
                if created:
                    a.save()
                v = Venue.objects.get(lfm_venue_id=venue)
                cdate = datetime.strptime(start_date, "%a, %d %b %Y %H:%M:%S")
                if int(cancelled) != 0:
                    cancelled = True
                else:
                    cancelled = False
                    
                c = ConcertDate(artist = a, venue = v, date = cdate, cancelled=cancelled, lfm_concert_id=lfm_concert_id)
                c.save()
        else:
            a, created = Artist.objects.get_or_create(name=artists)
            if created:
                a.save()
            v = Venue.objects.get(lfm_venue_id=venue)
            cdate = datetime.strptime(start_date, "%a, %d %b %Y %H:%M:%S")
            if int(cancelled) != 0:
                cancelled = True
            else:
                cancelled = False
                
            c = ConcertDate(artist = a, venue = v, date = cdate, cancelled=cancelled, lfm_concert_id=lfm_concert_id)
            c.save()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--debug", help="Run script in DEBUG mode", action="store_true")
    (options, args) = parser.parse_args()


    x = logging.getLogger("lastfm_scraper")
    f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s On Line: %(lineno)d %(message)s")
    h = logging.StreamHandler()
    h.setFormatter(f)

    if options.debug == True:
        x.setLevel(logging.DEBUG)
        x.addHandler(h)
    else:
        x.setLevel(logging.CRITICAL)
        x.addHandler(h)

    lg = logging.getLogger("lastfm_scraper")
    
    # last_fm initialize
    try:
        # read in session data. If it fails, we need to create it.
        lg.debug("Found a cached session key.")
        f = open(os.path.join(os.getenv('HOME'), '.lfm_session'), 'rb')
        SESSION_KEY = f.read()
        f.close()
    except:
        lg.debug("No Session Key Found! Creating One.")
        # sg = pylast.SessionKeyGenerator(LFM_API_KEY, LFM_SECRET)
        
        network = pylast.LastFMNetwork(api_key=LFM_API_KEY, api_secret=LFM_SECRET)
        sg = pylast.SessionKeyGenerator(network)
        # token = sg.getToken()
        auth_url = sg.get_web_auth_url()
        print "Please open the following URL in your web browser: %s" % (auth_url,)
        raw_input(">> Press Enter when Ready >>")
   
        data = sg.get_web_auth_session_key(auth_url)
   
        if data == types.NoneType:
            print "There was a problem with the authentication. Please try again."
            sys.exit(1)
        else:
            SESSION_KEY = str(data)
        
        f = open(os.path.join(os.getenv('HOME'), '.lfm_session'), 'wb')
        f.write(SESSION_KEY)
        f.close()
    
    lg.debug("LAST FM Session Key: %s" % (SESSION_KEY,))

    venues = get_venues()

    add_venues_to_database(venues)

    for venue in venues.keys():
        get_concerts_for_venue(venue)