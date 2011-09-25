import csv
import os
import settings
import re
from datetime import datetime
from django.core.management import setup_environ
project_directory = setup_environ(settings)
project_name = os.path.basename(project_directory)
os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % project_name

from wuzhear.hearapp.models import Artist, ConcertDate, Setlist, Song, Venue

def load_csv():
    jazzReader = csv.reader(open('jazzhistory.csv', 'rb'), delimiter='\t')
    for row in jazzReader:
        artist_name = row[0]
        artist, created = Artist.objects.get_or_create(name=artist_name)
        if created:
            artist.save()
        venue_name = row[2] 
        venue, created = Venue.objects.get_or_create(name=venue_name)
        if created:
            venue.save()
        
        
        #default everything to 7pm
        date = row[1].split(" at ")[0]
        print date
        date_obj = datetime.strptime(date, "%A %B %d, %Y")
        
        concert, created = ConcertDate.objects.get_or_create(artist = artist, venue = venue, date = date_obj)
        if created:
            concert.save


def main():
    load_csv()

if __name__== "__main__":
    main()