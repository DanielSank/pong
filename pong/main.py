import sys
import os
import config as C
import datetime


# sqlalchemy session
import sqlalchemy as sa
import sqlalchemy.orm as orm
engine = sa.create_engine(C.config['DB_URL'], echo=False)
Session = orm.sessionmaker(bind=engine)


import models as models
import forms


#from google.appengine.api import users
import jinja2
import webapp2 as wa2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class ViewGames(wa2.RequestHandler):
    def get(self):
        session = Session()
        games = session.query(models.Game).all()
        template = JINJA_ENVIRONMENT.get_template('view_games.html')
        self.response.write(template.render({'games': games}))


class AddGame(wa2.RequestHandler):

    def get(self):
        session = Session()
        players = [u.name for u in session.query(models.User).all()]
        form = forms.AddGame(players)
        template = JINJA_ENVIRONMENT.get_template('add_game.html')
        self.response.write(template.render({'form': form}))

    def post(self):
        session = Session()
        usernames = tuple([(u.name, u.name) for u in session.query(models.User).all()])
        form = forms.AddGame(self.request.POST)
        print self.request.POST
        form.playerA.choices = usernames
        form.playerB.choices = usernames
        if form.validate():
            print("FORM VALID")
            session = Session()
            game = models.Game(
                playerA=form.playerA.data,
                playerB=form.playerB.data,
                scoreA=form.scoreA.data,
                scoreB=form.scoreB.data,
                date=datetime.datetime.now())
            session.add(game)
            session.commit()
        else:
            print("OH NO")
        return wa2.redirect("/games/view")


class Users(wa2.RequestHandler):
    def get(self):
        session = Session()
        users = session.query(models.User).all()
        template = JINJA_ENVIRONMENT.get_template('users.html')
        self.response.write(template.render({
            'users': users,
            'form': forms.AddUser(),
        }))

    def post(self):
        form = forms.AddUser(self.request.POST)
        if form.validate():
            username = form.username.data
            session = Session()
            results = session.query(models.User).filter(models.User.name==username).all()
            if not results:
                user = models.User(name=username)
                session.add(user)
                session.commit()
            else:
                pass
                # TODO warn about adding repeated user name
            return wa2.redirect("/users")
        else:
            # TODO: pop up an error message
            return wa2.redirect("/users")


application = wa2.WSGIApplication([
    ('/users', Users),
    ('/games/add', AddGame),
    ('/games/view', ViewGames)
], debug=True)
