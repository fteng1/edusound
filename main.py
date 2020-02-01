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

class InputNotes(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/InputPage.html")
        self.response.write(start_template.render())
    def post(self):
        # expiration_string = self.request.get('expirationdate')
        # expiration_date = datetime.datetime.strptime(expiration_string, "%Y-%m-%d").date()
        #
        # # calendar_url = "http://www.google.com/calendar/event?action=TEMPLATE&text=%s&dates=%s/%s"
        # # calendar_link = calendar_url % ("TestEvent", 7, 12) #calendar_start, calendar_end)
        # # calendar_html = "<HTML><BODY><A href='%s' target='_blank'>Test Event Link</A></BODY></HTML>"
        # # self.response.write(calendar_html % calendar_link)
        # user = users.get_current_user()
        # food_input = self.request.get('addfooditem')
        #     #put into database (optional)
        # food_record = Food(food_name = food_input, user_id = user.user_id(), expiration_date = expiration_date)
        # food_record.put()
        self.redirect('/input')

class InputMusic(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/InputMusic.html")
        self.response.write(start_template.render())
    def post(self):
        # expiration_string = self.request.get('expirationdate')
        # expiration_date = datetime.datetime.strptime(expiration_string, "%Y-%m-%d").date()
        #
        # # calendar_url = "http://www.google.com/calendar/event?action=TEMPLATE&text=%s&dates=%s/%s"
        # # calendar_link = calendar_url % ("TestEvent", 7, 12) #calendar_start, calendar_end)
        # # calendar_html = "<HTML><BODY><A href='%s' target='_blank'>Test Event Link</A></BODY></HTML>"
        # # self.response.write(calendar_html % calendar_link)
        # user = users.get_current_user()
        # food_input = self.request.get('addfooditem')
        #     #put into database (optional)
        # food_record = Food(food_name = food_input, user_id = user.user_id(), expiration_date = expiration_date)
        # food_record.put()
        self.redirect('/inputmusic')

class Math(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/Math.html")
        self.response.write(start_template.render())
    def post(self):
        self.redirect('/math')

class Science(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/Science.html")
        self.response.write(start_template.render())
    def post(self):
        self.redirect('/science')

class CS(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/CS.html")
        self.response.write(start_template.render())
    def post(self):
        self.redirect('/cs')





#https://www.dw.com/image/48688022_303.jpg
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/inputnotes', InputNotes),
    ('/inputmusic', InputMusic),
    ('/math', Math),
    ('/science', Science),
    ('/cs', CS)

], debug=True)
