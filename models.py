from google.appengine.ext import ndb



class Note(ndb.Model):
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.StringProperty()
    owner = ndb.StringProperty()
    subject = ndb.StringProperty()
    title = ndb.StringProperty()

class Song(ndb.Model):
    title = ndb.StringProperty()
    artist = ndb.StringProperty()
    owner = ndb.StringProperty()
    subject = ndb.StringProperty()
    link = ndb.StringProperty()

class Subject(ndb.Model):
    name = ndb.StringProperty()
    owner = ndb.StringProperty()

class ModelWithUser(ndb.Model):
    nickname = ndb.StringProperty()
    user_id = ndb.StringProperty()
    joined_on = ndb.DateTimeProperty(auto_now_add=True) #changes when it is first created
    updated_on = ndb.DateTimeProperty(auto_now=True) #changes whenever its active
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

    @classmethod
    def get_by_user(cls, user):
        return cls.query().filter(cls.user_id == user.user_id()).get()
