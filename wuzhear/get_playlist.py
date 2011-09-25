import sys
import urllib2
import simplejson
import musicbrainz as m
import hmac


def get_grooveshark_song_ids(artist_name, concert_year):
    release_name = get_release_name(artist_name, concert_year)

    secret = "9099a07fe964eacc64a6cfc8141aa4ad"
    partial_url = "https://api.grooveshark.com/ws3.php?sig="

    params = '{"method":"getAlbumSearchResults","header":{"wsKey":"wuzhear"},"parameters":{"query":"'+release_name+'", "page":"1", "limit":"1"}}'

    digest_maker = hmac.new(secret)
    digest_maker.update(params)
    sig = digest_maker.hexdigest()

    opener = urllib2.build_opener()
    url = partial_url + sig
    f = urllib2.Request(url)
    response = opener.open(f, params)
    release_string = response.read()
    release_json = simplejson.loads(release_string)

    song_id_list = None;

    if 'result' in release_json:
        release_id = release_json['result']['albums'][0]['AlbumID'] 
        params = '{"method":"getAlbumSongs","header":{"wsKey":"wuzhear"},"parameters":{"albumID":"'+str(release_id)+'"}}'
        digest_maker = hmac.new(secret)
        digest_maker.update(params)
        sig = digest_maker.hexdigest()
        url = partial_url + sig
        f = urllib2.Request(url)
        response = opener.open(f, params)
        songs_string = response.read()
        songs_json = simplejson.loads(songs_string)
        song_id_list = []
        if 'result' in songs_json:
            for song_match in songs_json['result']['songs']:
                song_id_list.append(song_match['SongID'])
            
    return song_id_list
        

def get_release_name(artist_name, concert_year):
    #given an artist name and concert year, retrieve the most recent release during or before that year
    artist_matches = m.artist_search(artist_name)
    #ASSUMPTION: trust that the first match returned by musicbrainz is who we're after
    artist_id = artist_matches['artist-list'][0]['id']
    release_matches = m.get_artist_by_id(artist_id, includes=['releases'], release_status=['official'], release_type=['album'])
    releases = release_matches['artist']['release-list']

    #iterate over all releases, figure out their year of release
    #NOTE: we're overwriting multiple albums in the same year; we only end up with 1 per year
    years = {}
    for release in releases:
        years[int(release['date'][:4])] = release['title']

    #sort by year
    keys = years.keys()
    keys.sort()

    #RELEASE SELECTION LOGIC
       #if there have been no releases prior to or within 1 year of concert, just choose oldest release
    #if there are no releases at all, we're out of luck


    #declare our possible cases:
    release_near_concert_year = None
    most_recent_release_at_concert = None
    artists_oldest_release = None
    #is there more than one release?
    if len(keys) > 1:
        for key in keys:
            #if concert_year is within one year either side of the album release, the band probably played it
            if abs(concert_year - key) <= 1:
                release_near_concert_year = years[key]
            #otherwise, the band probably played their most recent release at the time of concert year
            if key < concert_year:
                most_recent_release_at_concert = years[key]

        if not release_near_concert_year and not most_recent_release_at_concert:
            #no release prior to the concert, so just choose the artist's oldest release
            artists_oldest_release = years[keys[0]]

    elif len(keys) == 1:
        #artist only released one album
        artists_oldest_release = years[keys[0]]

    #else we're screwed

    #now figure out what to return:
    if release_near_concert_year:
        release_to_return = release_near_concert_year
    elif most_recent_release_at_concert:
        release_to_return = most_recent_release_at_concert
    elif artists_oldest_release:
        release_to_return = artists_oldest_release
    #else we return None

    return release_to_return







def main():
    songs = get_grooveshark_song_ids("Chick Corea", 2009)
    for song in songs:
        print song + "\n"
	#print m.get_artist_by_id("952a4205-023d-4235-897c-6fdb6f58dfaa", [])
	#print m.get_label_by_id("aab2e720-bdd2-4565-afc2-460743585f16")
	#print m.get_release_by_id("e94757ff-2655-4690-b369-4012beba6114")
	#print m.get_release_group_by_id("9377d65d-ffd5-35d6-b64d-43f86ef9188d")
	#print m.get_recording_by_id("cb4d4d70-930c-4d1a-a157-776de18be66a")
	#print m.get_work_by_id("7e48685c-72dd-3a8b-9274-4777efb2aa75")

	#print m.get_releases_by_discid("BG.iuI50.qn1DOBAWIk8fUYoeHM-")
	#print m.get_recordings_by_puid("070359fc-8219-e62b-7bfd-5a01e742b490")
	#print m.get_recordings_by_isrc("GBAYE9300106")

	#m.auth("", "")
	#m.submit_barcodes({"e94757ff-2655-4690-b369-4012beba6114": "9421021463277"})
	#m.submit_puids({"cb4d4d70-930c-4d1a-a157-776de18be66a":"e94757ff-2655-4690-b369-4012beba6114"})
	#m.submit_tags(recording_tags={"cb4d4d70-930c-4d1a-a157-776de18be66a":["these", "are", "my", "tags"]})
	#m.submit_tags(artist_tags={"952a4205-023d-4235-897c-6fdb6f58dfaa":["NZ", "twee"]})

	#m.submit_ratings(recording_ratings={"cb4d4d70-930c-4d1a-a157-776de18be66a":20})

	#print m.get_recordings_by_echoprint("aryw4bx1187b98dde8")
	#m.submit_echoprints({"e97f805a-ab48-4c52-855e-07049142113d": "anechoprint1234567"})

if __name__ == "__main__":
	main()
