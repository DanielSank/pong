import wtforms as wtf
import wtforms.validators as validators


class AddUser(wtf.Form):
    username = wtf.StringField('Username', [validators.Length(min=4, max=12)])


class AddGame(wtf.Form):

    def __init__(self, formdata=None, players=None):
        super(AddGame, self).__init__(formdata=formdata)
        self.playerA.choices = [(p, p) for p in players]
        self.playerB.choices = [(p, p) for p in players]

    playerA = wtf.SelectField()
    playerB = wtf.SelectField()

    scoreA = wtf.SelectField(choices=[(i, i) for i in range(22)], coerce=int)
    scoreB = wtf.SelectField(choices=[(i, i) for i in range(22)], coerce=int)

    def validate(self):
        """Override default validation, checking for sensible game results."""
        if not wtf.Form.validate(self):
            return False
        ok = True
        if self.scoreA.data == self.scoreB.data:
            ok = False
        if self.playerA.data == self.playerB.data:
            ok = False
        return ok
