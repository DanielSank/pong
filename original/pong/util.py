import os
import webapp2 as wa2
import google.appengine.api.users as usersapi
import models


def user_exists(username, session):
    """Return True if username is registered, False otherwise"""
    q = session.query(models.User).filter(models.User.name==username)
    return session.query(q.exists()).scalar()


def user_wins(username, session):
    """Total number of wins for a user"""
    return session.query(models.Game).filter(
        models.Game.winner.has(name=username)).count()


def require_login(sqla_sessionmaker):
    def require_login_decorator(func):
        def wrapped(self, *args, **kw):
            user = usersapi.get_current_user()
            if not user:
                return wa2.redirect(usersapi.create_login_url(self.request.path))
            nickname = user.email().split('@')[0]
            if (usersapi.is_current_user_admin() or
                user_exists(nickname, sqla_sessionmaker())):
                return func(self, *args, **kw)
            else:
                # TODO: Deal with unallowed user
                self.response.write("""
                    <html>
                    <body>
                        <p>Hi, {}! You are not a registered user :(</p>
                        <p><a href="{}">logout</a></p>
                    </body>
                """.format(nickname, usersapi.create_logout_url(self.request.path)))
        return wrapped
    return require_login_decorator


def in_production_mode():
    """Get deployment environment.

    Returns (bool): True if in production mode, false otherwise.
    """
    if (os.getenv('SERVER_SOFTWARE') and
                os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
        mode = True
    else:
        mode = False
    return mode
