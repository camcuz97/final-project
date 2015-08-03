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

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))



class Song(ndb.Model):
    name = ndb.StringProperty(required = True)
    artist = ndb.StringProperty(required = True)
    genre = ndb.StringProperty(required = True)
    mood = ndb.StringProperty(required = True)

class Video(ndb.Model):
    name = ndb.StringProperty(required = True)
    author = ndb.StringProperty(required = True)
    keyword = ndb.StringProperty(required = True)

song1 = Song(name = "Headlines", artist = "Drake", genre =  "Hip-Hop", mood = "Happy")
song1.put()
vid1 = Video(name = "Kittehs", author = "Mr. Meowgi", keyword = "Purr")
vid1.put()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        my_vars = {'song':song1}
        main_page_template = jinja_environment.get_template('templates/main.html')
        self.response.out.write(main_page_template.render(my_vars))
        # self.response.write('Hello world!')

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
