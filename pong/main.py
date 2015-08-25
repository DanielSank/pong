import sys
import os
import config as C
import datetime


# sqlalchemy session
import sqlalchemy as sa
import sqlalchemy.orm as orm
engine = sa.create_engine(C.config['DB_URL'], echo=False)
Session = orm.sessionmaker(bind=engine)


import elo
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
    @util.require_login(Session)
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

    @util.require_login(Session)
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
                winner_name=form.winner.data,
                loser_name=form.loser.data,
                winner_score=form.winner_score.data,
                loser_score=form.loser_score.data,
                date=datetime.datetime.now())
            session.add(game)
            session.commit()
        else:
            print("FORM INVALID")
        return wa2.redirect("/games/view")


class Users(wa2.RequestHandler):
    @util.require_login(Session)
    def get(self):
        session = Session()
        users = session.query(models.User).all()
        wins = [util.user_wins(u.name, session) for u in users]
        template = JINJA_ENVIRONMENT.get_template('users.html')
        self.response.write(template.render({
            'users': zip(users, wins),
            'form': forms.AddUser(),
            'logout_url': usersapi.create_logout_url('/users')
        }))


class Ratings(wa2.RequestHandler):
    @util.require_login(Session)
    def get(self):
        session = Session()
        users = session.query(models.User).all()
        games = session.query(models.Game).all()
        ratings = dict((user.name, 500) for user in users)
        for g in games:
            r_winner = ratings[g.winner.name]
            r_loser = ratings[g.loser.name]
            g.winner_prev_rating = int(r_winner)
            g.loser_prev_rating = int(r_loser)
            r_winner, r_loser = elo.elo(r_winner, r_loser, g.winner_score + 11, g.loser_score)
            ratings[g.winner.name] = r_winner
            ratings[g.loser.name] = r_loser
            g.winner_new_rating = int(r_winner)
            g.loser_new_rating = int(r_loser)
            def with_sign(n):
                return ('+' if n >= 0 else '') + str(n)
            g.winner_move = with_sign(g.winner_new_rating - g.winner_prev_rating)
            g.loser_move = with_sign(g.loser_new_rating - g.loser_prev_rating)
        leader_board = reversed(sorted((int(ratings[u.name]), u.name)
                                       for u in users))
        template = JINJA_ENVIRONMENT.get_template('ratings.html')
        self.response.write(
            template.render({
                'games': games,
                'leader_board': leader_board,
                'logout_url': usersapi.create_logout_url(self.request.path)
            })
        )


class Error(wa2.RequestHandler):
    def get(self):
        raise Exception("If you see this you're not in production mode")


application = wa2.WSGIApplication([
    ('/users', Users),
    ('/games/add', AddGame),
    ('/games', ViewGames),
    ('/games/view', ViewGames),
    ('/ratings', Ratings),
    ('/error', Error)
], debug=not util.in_production_mode())
