import wtforms as wtf
import wtforms.validators as validators


class AddUser(wtf.Form):
    username = wtf.StringField('Username', [validators.Length(min=4, max=12)])


class AddGame(wtf.Form):

    def __init__(self, players):
        super(AddGame, self).__init__()
        self.playerA.choices = [(p, p) for p in players]
        self.playerB.choices = [(p, p) for p in players]

    playerA = wtf.SelectField()
    playerB = wtf.SelectField()

    scoreA = wtf.SelectField(choices=[(i, i) for i in range(22)], coerce=int)
    scoreB = wtf.SelectField(choices=[(i, i) for i in range(22)], coerce=int)

