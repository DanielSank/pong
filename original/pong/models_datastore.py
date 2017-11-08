from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()


class Game(ndb.Model):
    winner_score = ndb.IntegerProperty()
    loser_scope = ndb.IntegerProperty()

    winner = ndb.KeyProperty(kind=User)
    loser = ndb.KeyProperty(kind=User)

    date = ndb.DateTimeProperty(auto_now_add=True)
