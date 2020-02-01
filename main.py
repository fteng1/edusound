import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users
from models import ModelWithUser
from models import Event



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
        main_template = JINJA_ENVIRONMENT.get_template('log_in.html')
        self.response.write(main_template.render())









#https://www.dw.com/image/48688022_303.jpg
app = webapp2.WSGIApplication([
    ('/', MainPage),

], debug=True)
