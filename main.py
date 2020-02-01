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
        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))
        main_template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(main_template.render())

class InputNotesPage(webapp2.RequestHandler):
    def get(self):
        calendar_template = JINJA_ENVIRONMENT.get_template('InputNotes.html')
        user = users.get_current_user()
        self.response.write(calendar_template.render())

    def post(self):
        if self.request.get("action") == "Add to Notes":
            start_string = self.request.get("starttime")
            subject = self.request.get("subject-type")
            current_subject = Subject.query().filter(Subject.owner == user.user_id()).order(Subject.start).fetch()



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

], debug=True)
