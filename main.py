import webapp2
import jinja2
import os
import time

from google.appengine.ext import ndb
from google.appengine.api import users
from models import Note
from models import Song
from models import Subject
from models import ModelWithUser


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        #the code for the sign-in and -out button
        user = users.get_current_user()
        #if ModelWithUser.query().filter(ModelWithUser.user_id == user.user_id()).fetch(1) is not None:
        current_user = check_profile_exists(ModelWithUser())
        current_user.put()
        if user:
            logout_url = users.create_logout_url('/')
            if current_user is None:
                greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                    current_user.first_name, logout_url)
            else:
                greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                    current_user.nickname, logout_url)
        else:
            login_url = users.create_login_url('/welcome') #replace / with whatever url you want
            greeting = '<a href="{}">Sign in</a>'.format(login_url)
        #self.response.write(
        #   '<html><body>{}</body></html>'.format(greeting))
        main_template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(main_template.render(get_subject_dict()))

    def post(self):
        user = users.get_current_user()
        if self.request.get("action") == "Add Subject":
            subject_string = self.request.get("subject_string")
            subject = Subject(name=subject_string, owner=user.user_id())
            subject.put()
        time.sleep(0.1)
        self.redirect('/')

class InputNotesPage(webapp2.RequestHandler):
    def get(self):
        input_notes_template = JINJA_ENVIRONMENT.get_template('templates/InputNotes.html')
        user = users.get_current_user()
        self.response.write(input_notes_template.render(get_subject_dict()))

    def post(self):
        user = users.get_current_user()
        if self.request.get("action") == "Add to Notes":
            note = Note(text=self.request.get("notes_string"), owner=user.user_id(), subject=self.request.get("subject-type"))
            note.put()
        self.get()

class SubjectNotesPage(webapp2.RequestHandler):
    def get(self):
        # need to get the subject that was clicked
        if len(self.request.url.split('?')) > 1:
            subject_type = self.request.url.split('?')[1].replace('%', ' ')
        else:
            subject_type = ''
        user = users.get_current_user()
        subject_template = JINJA_ENVIRONMENT.get_template('templates/subjectNotes.html')
        notes = Note.query().filter(Note.owner == user.user_id() and Note.subject == subject_type).fetch()
        songs = Song.query().filter(Song.owner == user.user_id() and Song.subject == subject_type).fetch()
        subject_dict = {
            "notes_list": notes,
            "songs_list": songs,
            "subject_name": subject_type
        }
        self.response.write(subject_template.render(subject_dict))

class InputMusicPage(webapp2.RequestHandler):
    def get(self):
        input_music_template = JINJA_ENVIRONMENT.get_template('templates/InputMusic.html')
        user = users.get_current_user()
        self.response.write(input_music_template.render(get_subject_dict()))

    def post(self):
        user = users.get_current_user()
        if self.request.get("action") == "Add to Music":
            title_string = self.request.get("title_string")
            artist_string = self.request.get("artist_string")
            subject_string = self.request.get("subject-type")
            song_link = self.request.get("song_string")
            song = Song(link=song_link, title=title_string, artist=artist_string, owner=user.user_id(), subject=subject_string)
            song.put()
        self.get()

def check_profile_exists(value):
    user = users.get_current_user()
    my_profiles = ModelWithUser.query().filter(ModelWithUser.user_id == user.user_id()).fetch()
    if len(my_profiles) == 1:
        my_profile = my_profiles[0]
    else:
        my_profile = value #will either be None of the Profile creator class
        #my_profile = Profile()
        my_profile.user_id = user.user_id()
        my_profile.put()
    return my_profile

def get_subject_dict():
    user = users.get_current_user()
    subjects = Subject.query().filter(Subject.owner == user.user_id()).fetch()
    sub_dict = {
        "subject_list": subjects
    }
    return sub_dict

class DeleteHandler(webapp2.RequestHandler):
    def post(self):
        subject_id = self.request.get('subject_id')
        subject_key = ndb.Key(urlsafe = subject_id)
        note_id = self.request.get('note_id')
        note_key = nbd.Key(urlsafe = note_id)
        note_key.delete()
        subject_key.delete()
        time.sleep(0.1)
        self.redirect('/subject')




#https://www.dw.com/image/48688022_303.jpg
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/inputNotes', InputNotesPage),
    ('/subject', SubjectNotesPage),
    ('/songs', InputMusicPage),
    ('/inputMusic', InputMusicPage),
    ('/delete', DeleteHandler)
], debug=True)
