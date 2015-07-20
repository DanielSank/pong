import wtforms as wtf
import wtforms.validators as validators


class AddUser(wtf.Form):
    username = wtf.StringField('Username', [validators.Length(min=4, max=12)])


class AddGame(wtf.Form):

    playerA = wtf.SelectField()
    playerB = wtf.SelectField()

    scoreA = wtf.SelectField(choices=[(i, i) for i in range(22)], coerce=int)
    scoreB = wtf.SelectField(choices=[(i, i) for i in range(22)], coerce=int)

#    player1_score = wtf.SelectField(
#        choices=[(i, i) for i in range(22)])
#        validators = [
#            validators.NumberRange(min=0, message='Score must be positive')])

#    player2_score = wtf.SelectField(
#        choices=[(i, i) for i in range(22)])
#        validators = [
#            validators.NumberRange(min=0, message='Score must be positive')])


import models
import wtforms.ext.sqlalchemy.orm as sqla

# TODO: simpler sqla form
