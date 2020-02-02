import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users
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
        self.response.write(main_template.render())

class InputNotesPage(webapp2.RequestHandler):
    def get(self):
        input_notes_template = JINJA_ENVIRONMENT.get_template('templates/InputNotes.html')
        user = users.get_current_user()
        self.response.write(input_notes_template.render())

    def post(self):
        user = users.get_current_user()
        if self.request.get("action") == "Add to Notes":
            start_string = self.request.get("starttime")
            if start_string != "":
                start_date = datetime.strptime(start_string, "%Y-%m-%dT%H:%M")
                subject_type = self.request.get("subject-type")
                current_subject = Subject.query().filter(Subject.owner == user.user_id() and Subject.name == subject_type).fetch()
                if len(current_subject) == 1:
                    subject = current_subject[0]
                    subject.notes.append(Note(text=self.request.get("textbox")))
        self.get()

class SubjectPage(webapp2.RequestHandler):
    def get(self):
        # need to get the subject that was clicked
        subject_type = "math"
        user = users.get_current_user()
        subject_template = JINJA_ENVIRONMENT.get_template('templates/subjectNotes.html')
        subject = Subject.query().filter(Subject.owner == user.user_id() and Subject.name == subject_type).fetch()
        notes = []
        songs = []
        for sub in subject:
            notes.extend(sub.notes)
            songs.extend(sub.songs)
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
        self.response.write(input_music_template.render())

    def post(self):
        user = users.get_current_user()
        if self.request.get("action") == "Add to Music":
            title_string = self.request.get("title_string")
            artist_string = self.request.get("artist_string")
            current_subject = Subject.query().filter(Subject.owner == user.user_id() and Subject.name == subject_type).fetch()
            if len(current_subject) == 1:
                subject = current_subject[0]
                subject.notes.append(Song(title=title_string, artist=artist_string))
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










#https://www.dw.com/image/48688022_303.jpg
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/input', InputNotesPage),
    ('/subject', SubjectPage)
], debug=True)
