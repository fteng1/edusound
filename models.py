from google.appengine.ext import ndb

class ModelWithUser(ndb.Model):
    nickname = ndb.StringProperty()
    user_id = ndb.StringProperty()
    joined_on = ndb.DateTimeProperty(auto_now_add=True) #changes when it is first created
    updated_on = ndb.DateTimeProperty(auto_now=True) #changes whenever its active
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    profile_pic =ndb.StringProperty(default="https://cdn.pixabay.com/photo/2018/10/30/16/06/water-lily-3784022__340.jpg")

    @classmethod
    def get_by_user(cls, user):
        return cls.query().filter(cls.user_id == user.user_id()).get()

class Subject(ndb.Model):
    notes = ndb.StructuredProperty(Note, repeated=True)
    songs = ndb.StructuredProperty(Song, repeated=True)

class Note(ndb.Model):
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.StringProperty()

class Song(ndb.Model):
    title = ndb.StringProperty()
    artist = ndb.StringProperty()
