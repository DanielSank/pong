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

        init = 500

        # point-spread (ps) ratings
        ps_ratings, ps_history = elo.compute_ratings(
            [((g.winner.name, g.winner_score), (g.loser.name, g.loser_score))
             for g in games],
            init=init)

        # win-loss (wl) ratings
        wl_ratings, wl_history = elo.compute_ratings(
            [((g.winner.name, 1), (g.loser.name, 0))
             for g in games],
            init=init)

        for g, ps, wl in zip(games, ps_history, wl_history):
            ((ps_r_w, ps_dr_w), (ps_r_l, ps_dr_l)) = ps
            ((wl_r_w, wl_dr_w), (wl_r_l, wl_dr_l)) = wl
            g.winner_ps_rating = int(ps_r_w)
            g.loser_ps_rating = int(ps_r_l)
            g.winner_wl_rating = int(wl_r_w)
            g.loser_wl_rating = int(wl_r_l)
            def with_sign(n):
                return ('+' if n >= 0 else '') + str(n)
            g.winner_ps_move = with_sign(int(ps_dr_w))
            g.loser_ps_move = with_sign(int(ps_dr_l))
            g.winner_wl_move = with_sign(int(wl_dr_w))
            g.loser_wl_move = with_sign(int(wl_dr_l))

        ps_leader_board = reversed(sorted((int(ps_ratings.get(u.name, init)), u.name)
                                          for u in users))
        wl_leader_board = reversed(sorted((int(wl_ratings.get(u.name, init)), u.name)
                                          for u in users))

        template = JINJA_ENVIRONMENT.get_template('ratings.html')
        self.response.write(
            template.render({
                'games': games,
                'ps_leader_board': ps_leader_board,
                'wl_leader_board': wl_leader_board,
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
