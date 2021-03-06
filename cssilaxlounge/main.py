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


class User(ndb.Model):
    user_name = ndb.StringProperty(required = True)
    current_user_id = ndb.StringProperty(required = True)

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
    genre = ndb.KeyProperty(Genre, required = True)
    mood = ndb.StringProperty(required = True)
    spotify_html = ndb.StringProperty(required = True)

class Author(ndb.Model):
    author = ndb.StringProperty(required = True)

class Keyword(ndb.Model):
    name = ndb.StringProperty(required = True)

class Video(ndb.Model):
    name = ndb.StringProperty(required = True)
    author = ndb.StringProperty()
    keyword = ndb.KeyProperty(Keyword, repeated = True)
    corresponding_html = ndb.StringProperty(required = True)

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        home_page_template = jinja_environment.get_template('templates/home.html')
        user = users.get_current_user()
                #Comments below added playlists later, not needed for new users
                                    # hip_id = Genre.query(Genre.name == 'Hip-Hop').get().key.id()
                                    # hip_key = ndb.Key(Genre, int(hip_id))
                                    # punk_id = Genre.query(Genre.name == 'Punk').get().key.id()
                                    # punk_key = ndb.Key(Genre, int(punk_id))
                                    # pop_id = Genre.query(Genre.name == 'Pop').get().key.id()
                                    # pop_key = ndb.Key(Genre, int(pop_id))
                                    # alt_id = Genre.query(Genre.name == 'Alternative').get().key.id()
                                    # alt_key = ndb.Key(Genre, int(alt_id))
                                    #
                                    #
                                    # #ndb.Key(Genre, int())
                                    #
                                    # generic_hiphop = Playlist(genre = hip_key, mood = "Indifferent", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:spotify:playlist:5yolys8XG4q7YfjYGl5Lff" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                                    # generic_hiphop.put()
                                    # generic_punk = Playlist(genre = punk_key, mood = "Indifferent", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:spotify:playlist:0dBTRmxyfCYFY483cve71c" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                                    # generic_punk.put()
                                    # generic_alt = Playlist(genre = alt_key, mood = "Indifferent", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:spotify:playlist:2YoVrFsJPvunjHQYfM12cP" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                                    # generic_alt.put()
                                    # generic_pop = Playlist(genre = pop_key, mood = "Indifferent", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:spotify:playlist:5FJXhjdILmRA2z5bvz4nzf" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                                    # generic_pop.put()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            my_vars = {'user': user.nickname()}
            main_page_template = jinja_environment.get_template('templates/home.html')
            self.response.out.write(home_page_template.render(my_vars))
            current_user = User(user_name = user.nickname(), current_user_id = user.user_id())
            existing_user = User.query().filter(User.current_user_id == current_user.current_user_id).fetch()\
            
            if not existing_user:
                keyword1 = Keyword(name = "funny")
                keyword2 = Keyword(name = "intriguing")
                keyword3 = Keyword(name = "relaxing")
                keyword4 = Keyword(name = "educational")
                keyword5 = Keyword(name = "ted_talk")
                keyword6 = Keyword(name = "fails")

                keyword1.put()
                keyword2.put()
                keyword3.put()
                keyword4.put()
                keyword5.put()
                keyword6.put()

                funny_video_1 = Video(name = "funny game show answers", keyword = [keyword1.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/R7ghDhpCLKM" frameborder="0" allowfullscreen></iframe>')
                funny_video_2 = Video(name = "America's Funniest Home Videos Compilation", keyword = [keyword1.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/W4wb5r-FNTc" frameborder="0" allowfullscreen></iframe>')
                funny_video_3 = Video(name = "April Fools Prank", keyword = [keyword1.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/R9rymEWJX38" frameborder="0" allowfullscreen></iframe>')

                funny_video_1.put()
                funny_video_2.put()
                funny_video_3.put()

                intriguing_video_1 = Video(name = "intriguing facts about the human brain", keyword = [keyword2.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/XQKDd_SjMJA" frameborder="0" allowfullscreen></iframe>')
                intriguing_video_2 = Video(name = "10 obscure intriguing facts", keyword = [keyword2.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/f8sW_tv0WRI" frameborder="0" allowfullscreen></iframe>')
                intriguing_video_3 = Video(name = "intriguing people", keyword = [keyword2.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/Up5eLfjdjEM" frameborder="0" allowfullscreen></iframe>')

                intriguing_video_1.put()
                intriguing_video_2.put()
                intriguing_video_3.put()

                relaxing_video_1 = Video(name = "relaxing kaleidoscope", keyword = [keyword3.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/q2fIWB8o-bs" frameborder="0" allowfullscreen></iframe>')
                relaxing_video_2 = Video(name = "relaxing nature", keyword = [keyword3.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/kkbmijuAvlM" frameborder="0" allowfullscreen></iframe>')
                relaxing_video_3 = Video(name = "relaxing stargazing", keyword = [keyword3.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/HXT38GS1Hrw" frameborder="0" allowfullscreen></iframe>')

                relaxing_video_1.put()
                relaxing_video_2.put()
                relaxing_video_3.put()

                educational_video_1 = Video(name = "Pluto's First Encounter", keyword = [keyword4.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/rYg7rMgJuNQ" frameborder="0" allowfullscreen></iframe>')
                educational_video_2 = Video(name = "Navy Seals Documentary", keyword = [keyword4.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/yAgKnwJQYUs" frameborder="0" allowfullscreen></iframe>')
                educational_video_3 = Video(name = "Jane Goodall on Chimpanzee's", keyword = [keyword4.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/LKyrLFyOi04" frameborder="0" allowfullscreen></iframe>')

                educational_video_1.put()
                educational_video_2.put()
                educational_video_3.put()

                ted_video_1 = Video(name = "Temple Grandin on Autism Brains", keyword = [keyword5.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/fn_9f5x0f1Q" frameborder="0" allowfullscreen></iframe>')
                ted_video_2 = Video(name = "Larry Page on Where Google is going", keyword = [keyword5.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/mArrNRWQEso" frameborder="0" allowfullscreen></iframe>')
                ted_video_3 = Video(name = "Gavin Schmidt on the Environment", keyword = [keyword5.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/JrJJxn-gCdo" frameborder="0" allowfullscreen></iframe>')

                ted_video_1.put()
                ted_video_2.put()
                ted_video_3.put()

                fail_video_1 = Video(name = "Water sport fails", keyword = [keyword6.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/ufU7ZkAn0GI" frameborder="0" allowfullscreen></iframe>')
                fail_video_2 = Video(name = "Track fails", keyword = [keyword6.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/iDicTJwqhl4" frameborder="0" allowfullscreen></iframe>')
                fail_video_3 = Video(name = "Trampoline fails", keyword = [keyword6.key], corresponding_html = '<iframe width="560" height="315" src="https://www.youtube.com/embed/EmP2JHUTisg" frameborder="0" allowfullscreen></iframe>')

                fail_video_1.put()
                fail_video_2.put()
                fail_video_3.put()

                genre1 = Genre(name = "Hip-Hop")
                genre2 = Genre(name = "Punk")
                genre3 = Genre(name = "Alternative")
                genre4 = Genre(name = "Pop")
                genre1.put()
                genre2.put()
                genre3.put()
                genre4.put()
                happy_punk = Playlist(genre = genre2.key, mood = "Happy", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:1248161175:playlist:6SiRKZR8I6sGkZvrc1axbm" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                happy_punk.put()
                angry_punk = Playlist(genre = genre2.key, mood = "Angry", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:1248161175:playlist:1B8lmAiamPhWhffvWQMFkc" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                angry_punk.put()
                sad_punk = Playlist(genre = genre2.key, mood = "Sad", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:1248161175:playlist:5A5yeeWsT5K11CRIm7PLbL" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                sad_punk.put()
                chill_punk = Playlist(genre = genre2.key, mood = "Chill", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:1248161175:playlist:2ED4mB5roq8K5ZB1mw2GSq" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                chill_punk.put()
                happy_hiphop = Playlist(genre = genre1.key, mood = "Happy", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:1248161175:playlist:707VPhsNKJmGgzxfVAQ8m6" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                happy_hiphop.put()
                angry_hiphop = Playlist(genre = genre1.key, mood = "Angry", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:1248161175:playlist:5PXFRxTNZAqEmJcZY0AkAf" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                angry_hiphop.put()
                sad_hiphop = Playlist(genre = genre1.key, mood = "Sad", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:1248161175:playlist:3VoZw4XMfiwI0qLjn26CFs" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                sad_hiphop.put()
                chill_hiphop = Playlist(genre = genre1.key, mood = "Chill", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:1248161175:playlist:55Dcl4ZbCWWkvfZhp4cp3Q" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                chill_hiphop.put()
                happy_pop = Playlist(genre = genre4.key, mood = "Happy", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:1248161175:playlist:3K6F139jLrvC8BIug62tAp" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                happy_pop.put()
                angry_pop = Playlist(genre = genre4.key, mood = "Angry", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:1248161175:playlist:76XycdWsdprBsu31rIeobf" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                angry_pop.put()
                sad_pop = Playlist(genre = genre4.key, mood = "Sad", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:4540545111:playlist:34EzzQ8tgpBeXk5JppR1XS" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                sad_pop.put()
                chill_pop = Playlist(genre = genre4.key, mood = "Chill", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:spotify:playlist:6gTlyWrX5XJqU9J4sZfNj4" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                chill_pop.put()
                happy_alt = Playlist(genre = genre3.key, mood = "Happy", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:12139929588:playlist:3Z4yQt3TNTQC15YqUXpINh" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                happy_alt.put()
                angry_alt = Playlist(genre = genre3.key, mood = "Angry", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:1248161175:playlist:0L5BbmKIanbvcGjezB97KQ" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                angry_alt.put()
                sad_alt = Playlist(genre = genre3.key, mood = "Sad", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:kkt_topol:playlist:5tPAmcKqoBrGChGO6lMuHu" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                sad_alt.put()
                chill_alt = Playlist(genre = genre3.key, mood = "Chill", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:spotify:playlist:0XUlpafP8eIlIWt3VHSd7q" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                chill_alt.put()
                generic_hiphop = Playlist(genre = genre1.key, mood = "Indifferent", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:spotify:playlist:5yolys8XG4q7YfjYGl5Lff" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                generic_hiphop.put()
                generic_punk = Playlist(genre = genre2.key, mood = "Indifferent", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:spotify:playlist:0dBTRmxyfCYFY483cve71c" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                generic_punk.put()
                generic_alt = Playlist(genre = genre3.key, mood = "Indifferent", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:spotify:playlist:2YoVrFsJPvunjHQYfM12cP" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                generic_alt.put()
                generic_pop = Playlist(genre = genre4.key, mood = "Indifferent", spotify_html = '<iframe src="https://embed.spotify.com/?uri=spotify:user:spotify:playlist:5FJXhjdILmRA2z5bvz4nzf" width="800" height="470" frameborder="0" allowtransparency="true"></iframe>')
                generic_pop.put()

                current_user.put()

class RelaxHandler(webapp2.RequestHandler):
    def get(self):
        relax_page_template = jinja_environment.get_template('templates/relax.html')
        self.response.out.write(relax_page_template.render())

class VideoHandler(webapp2.RequestHandler):
    def get(self):
        video_page_template = jinja_environment.get_template('templates/video.html')
        keyword = self.request.get('keyword')
        if keyword:
            keyword_key = Keyword.query(Keyword.name == keyword).get().key
            #logging.info("Keyword:" + str(keyword_key))
            filtered_video_answer = Video.query(Video.keyword == keyword_key).fetch()
            filtered_vid_answer = []
            for vid in filtered_video_answer:
                filtered_vid_answer.append(str(vid.corresponding_html))
            #logging.info("Answers: "  + str(filtered_video_answer))
            vid_vars = {'video_html': filtered_vid_answer}
            if filtered_video_answer:
                self.response.out.write(video_page_template.render(vid_vars))
        else:
                self.response.out.write(video_page_template.render())


class MusicHandler(webapp2.RequestHandler):
    def get(self):
        music_page_template = jinja_environment.get_template('templates/music.html')
        mood = self.request.get('mood')
        genre = self.request.get('genre')
        if genre and mood:
            genre_key = Genre.query(Genre.name == genre).get().key
            filtered_answer = Playlist.query(Playlist.genre == genre_key, Playlist.mood == mood).fetch()
            my_vars = {'spotify_html': filtered_answer[0].spotify_html}
            if filtered_answer:
                self.response.out.write(music_page_template.render(my_vars))
                #for playlist in filtered_answer:
                    #self.response.write('<p align = "center">%s</p>'%playlist.spotify_html)
        else:
            self.response.out.write(music_page_template.render())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        about_page_template = jinja_environment.get_template('templates/about.html')
        self.response.out.write(about_page_template.render())



app = webapp2.WSGIApplication([
#    ('/', MainHandler),
    ('/', HomeHandler),
    ('/music', MusicHandler),
    ('/video', VideoHandler),
    ('/relax', RelaxHandler),
    ('/about', AboutHandler)
], debug=False) #DON'T FORGET TO SWITCH TO FALSE AT THE END
