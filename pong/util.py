import webapp2 as wa2
import google.appengine.api.users as usersapi
import models


def get_allowed_usernames(session):
    """Get list of all registered user names"""
    return [u.name for u in session.query(models.User).all()]


def require_login(url, sqla_sessionmaker):
    def require_login_decorator(func):
        def wrapped(self):
            user = usersapi.get_current_user()
            allowed_usernames = get_allowed_usernames(sqla_sessionmaker())
            print allowed_usernames
            if user:
                nickname = user.email().split('@')[0]
                if nickname in allowed_usernames:
                    func(self)
                else:
                    print("User {} not allowed".format(nickname))
                    self.response.write("nope")
            else:
                return wa2.redirect(usersapi.create_login_url(url))
        return wrapped
    return require_login_decorator
