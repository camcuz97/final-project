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


class Artist(ndb.Model):
    name = ndb.StringProperty(required = True)

class Genre(ndb.Model):
    name = ndb.StringProperty(required = True)

class UserModel(ndb.Model):
    currentUser = ndb.StringProperty(required = True)


class Song(ndb.Model):
    name = ndb.StringProperty(required = True)
    artist = ndb.KeyProperty(Artist, required = True)
    genre = ndb.KeyProperty(Genre, repeated = True)
    mood = ndb.StringProperty(repeated = True)


class Author(ndb.Model):
    author = ndb.StringProperty(required = True)

class Keyword(ndb.Model):
    keyword = ndb.StringProperty(required = True)


class Video(ndb.Model):
    name = ndb.StringProperty(required = True)
    author = ndb.KeyProperty(Author, required = True)
    keyword = ndb.KeyProperty(Keyword, required = True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        main_page_template = jinja_environment.get_template('templates/main.html')
        self.response.out.write(main_page_template.render())
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
        # song1 = Song(name = "Headlines",artist = artist1.key , genre = [genre1.key], mood = ["Happy"])
        # song2 = Song(name = "Crooked Young", artist = artist2.key, genre = [genre2.key], mood = ["Angry"])
        # song3 = Song(name = "Forever Young", artist = artist3.key, genre = [genre1.key], mood = ["Chilled"])
        # song4 = Song(name = "Terrible Things", artist = artist4.key, genre = [genre2.key], mood = ["Sad"])
        # song1.put()
        # song2.put()
        # song3.put()
        # song4.put()
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.response.write(user)
            main_page_template = jinja_environment.get_template('templates/main.html')

    def post(self):
        mood = self.request.get('mood') #recieves mood. Eventually will get mood and genre and use them to get items from datastore


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        home_page_template = jinja_environment.get_template('templates/home.html')
        self.response.out.write(home_page_template.render())


class VideoHandler(webapp2.RequestHandler):
    def get(self):
        video_page_template = jinja_environment.get_template('templates/video.html')
        self.response.out.write(video_page_template.render())


class MusicHandler(webapp2.RequestHandler):
    def get(self):
        music_page_template = jinja_environment.get_template('templates/music.html')
        self.response.out.write(music_page_template.render())
        # mood = "Chilled"
        # genre = "Hip-Hop"
        mood = self.request.get('mood')
        genre = self.request.get('genre')
        if  genre and mood:
            genre_key = Genre.query(Genre.name == genre).get().key
            logging.info("Geeeeenre:" + str(genre_key))
            logging.info("Moooooood: " + mood)
            filtered_answer = Song.query().filter(Song.genre == genre_key and Song.mood == mood).fetch()
            logging.info("Answers: "  + str(filtered_answer))
            # all_songs = Song.query().fetch()
            if filtered_answer:
                for song in filtered_answer:
                    self.response.write(song.name)
            else:
                self.response.write("Nope")
    # def post(self):
        # mood = self.request.get('mood')
        # genre = self.request.get('genre')


# class Video(self):
#     def __init__(self, name, uploader):
#         self.name = name
#         self.uploader = uploader
#
# video1 = Video("Hi", "Me")
# print video1.name
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/home', HomeHandler),
    ('/music', MusicHandler),
    ('/video', VideoHandler)
], debug=True) #DON'T FORGET TO SWITCH TO FALSE AT THE END
