#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
from google.appengine.api import users


jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class UserModel(ndb.Model):
    currentUser = ndb.StringProperty(required = True)

class Artist(ndb.Model):
    name = ndb.StringProperty(required = True)

class Genre(ndb.Model):
    name = ndb.StringProperty(required = True)

class Song(ndb.Model):
    name = ndb.StringProperty(required = True)
    artist = ndb.KeyProperty(Artist, required = True)
    genre = ndb.KeyProperty(Genre, repeated = True)
    mood = ndb.StringProperty(repeated = True)
    spotify_html = ndb.StringProperty(required = True)

class Playlist(ndb.Model):
    genre = ndb.KeyProperty(Genre, repeated = True)
    mood = ndb.StringProperty(repeated = True)
    spotify_html = ndb.StringProperty(required = True)

class Author(ndb.Model):
    author = ndb.StringProperty(required = True)

class Keyword(ndb.Model):
    name = ndb.StringProperty(required = True)


class Video(ndb.Model):
    name = ndb.StringProperty(required = True)
    author = ndb.StringProperty()
    keyword = ndb.KeyProperty(Keyword, repeated = True)
    corresponding_url = ndb.StringProperty(required = True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        main_page_template = jinja_environment.get_template('templates/main.html')
        self.response.out.write(main_page_template.render())

        # keyword1 = Keyword(name = "funny")
        # keyword1.put()
        # keyword2 = Keyword(name = "intriguing")
        # keyword2.put()
        # keyword3 = Keyword(name = "relaxing")
        # keyword3.put()
        # keyword4 = Keyword(name = "educational")
        # keyword4.put()
        # video1 = Video(name = "funny game show answers" , keyword = [keyword1.key], corresponding_url = "https://www.youtube.com/watch?v=R7ghDhpCLKM")
        # video1.put()
        # video2 = Video(name = "intriguing fact about the human brain", keyword = [keyword2.key], corresponding_url = "https://www.youtube.com/watch?v=XQKDd_SjMJA")
        # video2.put()
        # video3 = Video(name = "relaxing kaleidoscpoic images", keyword = [keyword3.key], corresponding_url = "https://www.youtube.com/watch?v=q2fIWB8o-bs")
        # video3.put()
        # video4 = Video(name = "educational video about technology and nature", keyword = [keyword4.key], corresponding_url = "https://www.youtube.com/watch?v=POsXsOY71W0")
        # video4.put()


        user = users.get_current_user()
        my_vars = {'user': user}
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            main_page_template = jinja_environment.get_template('templates/main.html')
            self.response.out.write(main_page_template.render(my_vars))
        # artist1 = Artist(name = "Drake")
        # artist1.put()
        # artist2 = Artist(name = "Bring me the Horizon")
        # artist2.put()
        # artist3 = Artist(name = "Jay-Z")
        # artist3.put()
        # artist4 = Artist(name = "Mayday Parade")
        # artist4.put()
        # genre1 = Genre(name = "Hip-Hop")
        # genre1.put()
        # genre2 = Genre(name = "Punk")
        # genre2.put()
        # song1 = Song(name = "Headlines",artist = artist1.key , genre = [genre1.key], mood = ["Happy"], spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:track:3XWZ7PNB3ei50bTPzHhqA6" width="300" height="80" frameborder="0" allowtransparency="true"></iframe>')
        # song2 = Song(name = "Crooked Young", artist = artist2.key, genre = [genre2.key], mood = ["Angry"], spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:track:3XWZ7PNB3ei50bTPzHhqA6" width="300" height="80" frameborder="0" allowtransparency="true"></iframe>')
        # song3 = Song(name = "Forever Young", artist = artist3.key, genre = [genre1.key], mood = ["Chilled"], spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:track:3XWZ7PNB3ei50bTPzHhqA6" width="300" height="80" frameborder="0" allowtransparency="true"></iframe>')
        # song4 = Song(name = "Terrible Things", artist = artist4.key, genre = [genre2.key], mood = ["Sad"], spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:track:3XWZ7PNB3ei50bTPzHhqA6" width="300" height="80" frameborder="0" allowtransparency="true"></iframe>')
        # song1.put()
        # song2.put()
        # song3.put()
        # song4.put()
        # happy_punk = Playlist(genre = [genre2.key], mood = ["Happy"], spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:spotify_france:playlist:5vUFrhjhYHJM1oAO50yLJS" width="300" height="380" frameborder="0" allowtransparency="true"></iframe>')
        # happy_punk.put()

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        home_page_template = jinja_environment.get_template('templates/home.html')
        self.response.out.write(home_page_template.render())


class VideoHandler(webapp2.RequestHandler):
    def get(self):
        video_page_template = jinja_environment.get_template('templates/video.html')
        self.response.out.write(video_page_template.render())
        keyword = self.request.get('keyword')
        if keyword:
            keyword_key = Keyword.query(Keyword.name == keyword).get().key
            logging.info("Keyword:" + str(keyword_key))
            filtered_video_answer = Video.query().filter(Video.keyword == keyword_key).fetch()
            logging.info("Answers: "  + str(filtered_video_answer))
            # all_songs = Song.query().fetch()
            if filtered_video_answer:
                for video in filtered_video_answer:
                    self.response.write(video.name)
                    self.response.write(video.corresponding_url)
            else:
                self.response.write("No corresponding video")

class MusicHandler(webapp2.RequestHandler):
    def get(self):
        music_page_template = jinja_environment.get_template('templates/music.html')
        self.response.out.write(music_page_template.render())
        # mood = "Chilled"
        # genre = "Hip-Hop"
        mood = self.request.get('mood')
        genre = self.request.get('genre')
        # if  genre and mood:
        #     genre_key = Genre.query(Genre.name == genre).get().key
        #     filtered_answer = Song.query().filter(Song.genre == genre_key and Song.mood == mood).fetch()
        #     my_vars = {}
        #     for song in filtered_answer:
        #         my_vars[str(song.name)] = str(song.spotify_html)
        #     logging.info(my_vars)
        #     # all_songs = Song.query().fetch()
        #     if filtered_answer:
        #         for song in filtered_answer:
        #             self.response.write('<p align = "center"> %s </p'%song.spotify_html)
        #             #self.response.write(str(song.spotify_html) + "<br>")
        #     else:
        #         self.response.write("Nope")
        if genre and mood:
            genre_key = Genre.query(Genre.name == genre).get().key
            filtered_answer = Playlist.query().filter(Playlist.genre == genre_key and Playlist.mood == mood).fetch()
            if filtered_answer:
                for playlist in filtered_answer:
                    self.response.write('<p align = "center"> %s </p'%playlist.spotify_html)
    # def post(self):
        # mood = self.request.get('mood')
        # genre = self.request.get('genre')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/home', HomeHandler),
    ('/music', MusicHandler),
    ('/video', VideoHandler)
], debug=True) #DON'T FORGET TO SWITCH TO FALSE AT THE END
