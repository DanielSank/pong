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
import util


import jinja2
import webapp2 as wa2
import google.appengine.api.users as usersapi


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class ViewGames(wa2.RequestHandler):
    @util.require_login('/games/view', Session)
    def get(self):
        session = Session()
        games = session.query(models.Game).all()
        template = JINJA_ENVIRONMENT.get_template('view_games.html')
        self.response.write(
            template.render(
                {'games': games,
                 'logout_url': usersapi.create_logout_url('/games')}
            )
        )


class AddGame(wa2.RequestHandler):

    @util.require_login('/games/add', Session)
    def get(self):
        session = Session()
        players = [u.name for u in session.query(models.User).all()]
        form = forms.AddGame(formdata=None, players=players)
        template = JINJA_ENVIRONMENT.get_template('add_game.html')
        self.response.write(
            template.render(
                {'form': form,
                'logout_url': usersapi.create_logout_url('/games')}
            )
        )

    def post(self):
        session = Session()
        usernames = [u.name for u in session.query(models.User).all()]
        form = forms.AddGame(formdata=self.request.POST, players=usernames)
        if form.validate():
            print("FORM VALID")
            session = Session()
            game = models.Game(
                playerA_name=form.playerA.data,
                playerB_name=form.playerB.data,
                scoreA=form.scoreA.data,
                scoreB=form.scoreB.data,
                date=datetime.datetime.now())
            session.add(game)
            session.commit()
        else:
            print("FORM INVALID")
        return wa2.redirect("/games/view")


class Users(wa2.RequestHandler):
    @util.require_login('/users', Session)
    def get(self):
        session = Session()
        users = session.query(models.User).all()
        template = JINJA_ENVIRONMENT.get_template('users.html')
        self.response.write(template.render({
            'users': users,
            'form': forms.AddUser(),
            'logout_url': usersapi.create_logout_url('/users')
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


class Error(wa2.RequestHandler):
    def get(self):
        raise Exception("If you see this you're not in production mode")


application = wa2.WSGIApplication([
    ('/users', Users),
    ('/games/add', AddGame),
    ('/games', ViewGames),
    ('/games/view', ViewGames),
    ('/error', Error)
], debug=not util.in_production_mode())
