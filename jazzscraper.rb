#!/usr/bin/ruby
require 'rubygems'
require 'mechanize'

agent = Mechanize.new

#grab the links to all artist pages (one page of artists for each letter)
top_page = agent.get("http://www.montrealjazzfest.com/artists/Default.aspx")
artist_letters = top_page.search("#rechArtNavLettre li a")

#every letter has its own page of artists
artist_letters.each do |letter|
  artists_page = agent.get("http://www.montrealjazzfest.com" + letter.attributes["href"].inner_html)
  artists = artists_page.search(".artistes3Col p a")
  artists.each do |artist|
    begin
      sleep 0.1
      artist_name = artist.inner_html
      artist_page = agent.get("http://www.montrealjazzfest.com/artists/" + artist.attributes["href"].inner_html)
      performances = artist_page.search(".artisteConcerts tr[valign=\"top\"]")
      performances.each do |performance| 
        act_name = performance.at(".artConcertTitre a").inner_html
        datevenue = performance.at(".artConcertDateLieu").inner_html.gsub(/\r\n\s*/, "")
        datevenue =~ /(.*)<br>(.*)/
        date = $1
        venue = $2

        #print!!!!
        print artist_name + "\t" + date + "\t" + venue  + "\t" + act_name + "\n"
      end
    rescue 
      next
    end
  end
end
  
  