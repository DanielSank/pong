import os
import datetime

import google.appengine.api.users as usersapi
import jinja2
import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlemon
import webapp2 as wa2

import pong.elo as elo
import pong.forms as forms
import pong.models as models
import secrets
import pong.util as util


# sqlalchemy session
session_maker = sqlemon.get_sessionmaker(
        'pong',
        None,
        secrets.CLOUD_SQL_PASSWORD)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Home(wa2.RequestHandler):
    @util.require_login(session_maker)
    def get(self):
        return wa2.redirect('/users')


class ViewGames(wa2.RequestHandler):
    @util.require_login(session_maker)
    def get(self):
        session = session_maker()
        games = session.query(models.Game).all()
        template = JINJA_ENVIRONMENT.get_template('view_games.html')
        content = template.render({
            'games': reversed(games),
            'logout_url': usersapi.create_logout_url('/games'),
            'is_admin_user': usersapi.is_current_user_admin()
        })
        self.response.write(content)


class AddGame(wa2.RequestHandler):

    @util.require_login(session_maker)
    def get(self):
        session = session_maker()
        players = [u.name for u in session.query(models.User).all()]
        form = forms.AddGame(formdata=None, players=players)
        template = JINJA_ENVIRONMENT.get_template('add_game.html')
        content = template.render({
            'form': form,
            'logout_url': usersapi.create_logout_url('/games'),
            'is_admin_user': usersapi.is_current_user_admin()
        })
        self.response.write(content)

    def post(self):
        session = session_maker()
        usernames = [u.name for u in session.query(models.User).all()]
        form = forms.AddGame(formdata=self.request.POST, players=usernames)
        if form.validate():
            print("FORM VALID")
            session = session_maker()
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
    @util.require_login(session_maker)
    def get(self):
        session = session_maker()
        users = session.query(models.User).all()
        wins = [util.user_wins(u.name, session) for u in users]
        template = JINJA_ENVIRONMENT.get_template('users.html')
        content = template.render({
            'users': zip(users, wins),
            'form': forms.AddUser(),
            'logout_url': usersapi.create_logout_url('/users'),
            'is_admin_user': usersapi.is_current_user_admin()
        })
        self.response.write(content)

    def post(self):
        form = forms.AddUser(formdata=self.request.POST)
        if form.validate():
            print("FORM VALID")
            session = session_maker()
            user = models.User(name=form.username.data)
            session.add(user)
            session.commit()
        else:
            print("FORM INVALID")
        return wa2.redirect(self.request.path)


class Ratings(wa2.RequestHandler):
    @util.require_login(session_maker)
    def get(self):
        session = session_maker()
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

        ps_leader_board = reversed(sorted((int(r), name) for name, r in ps_ratings.items()))
        wl_leader_board = reversed(sorted((int(r), name) for name, r in wl_ratings.items()))

        template = JINJA_ENVIRONMENT.get_template('ratings.html')
        content = template.render({
            'games': reversed(games),
            'ps_leader_board': ps_leader_board,
            'wl_leader_board': wl_leader_board,
            'logout_url': usersapi.create_logout_url(self.request.path),
            'is_admin_user': usersapi.is_current_user_admin()
        })
        self.response.write(content)


class User(wa2.RequestHandler):
    @util.require_login(session_maker)
    def get(self, name):
        session = session_maker()
        username = name
        user = session.query(models.User).filter(models.User.name==username).one()
        games = session.query(models.Game).filter(sa.or_(
            models.Game.winner==user,
            models.Game.loser==user)).all()

        matchup_data = {}  # opponent name -> data
        total_points = 0

        for game in games:
            opponent = game.loser_name if game.winner_name == username else game.winner_name
            d = matchup_data.setdefault(opponent, {
                'games_won': 0,
                'games_lost': 0,
                'points_won': 0,
                'points_lost': 0})
            if game.winner_name == username:
                game_win_loss_key = 'games_won'
                points_won_key = 'winner_score'
                points_lost_key = 'loser_score'
            else:
                game_win_loss_key = 'games_lost'
                points_won_key = 'loser_score'
                points_lost_key = 'winner_score'

            d[game_win_loss_key] += 1
            d['points_won'] += getattr(game, points_won_key)
            d['points_lost'] += getattr(game, points_lost_key)
            total_points += getattr(game, points_won_key)

        matchup_data = [(opponent, (d['games_won'],
                                    d['games_lost'],
                                    d['points_won'],
                                    d['points_lost']))
                        for opponent, d in matchup_data.items()]
        template = JINJA_ENVIRONMENT.get_template('user.html')
        content = template.render({
            'user_name': username,
            'total_games': len(games),
            'total_wins': sum(x[1][0] for x in matchup_data),
            'total_points': total_points,
            'matchup_data': matchup_data,
            'logout_url': usersapi.create_logout_url(self.request.path),
            'is_admin_user': usersapi.is_current_user_admin()
        })
        self.response.write(content)


class UserDel(wa2.RequestHandler):

    def post(self, name):
        form = forms.DelUser(formdata=self.request.POST)
        if form.validate():
            print("FORM VALID")
            session = session_maker()
            user = session.query(models.User).filter(models.User.name==name).one()
            session.delete(user)
            session.commit()
        else:
            print("FORM INVALID")
        return wa2.redirect("/users")


class Error(wa2.RequestHandler):
    def get(self):
        raise Exception("If you see this you're not in production mode")


application = wa2.WSGIApplication([
    ('/', Home),
    ('/users', Users),
    wa2.Route('/users/<name>', handler=User),
    wa2.Route('/users/<name>/del', handler=UserDel),
    ('/games/add', AddGame),
    ('/games', ViewGames),
    ('/games/view', ViewGames),
    ('/ratings', Ratings),
    ('/error', Error)
], debug=not sqlemon.production_mode())
