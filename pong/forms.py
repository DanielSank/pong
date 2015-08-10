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

    scoreA = wtf.IntegerField()
    scoreB = wtf.IntegerField()

    def validate(self):
        """Override default validation, checking for sensible game results."""
        if not wtf.Form.validate(self):
            return False

        ok = True
        if self.scoreA.data == self.scoreB.data:
            ok = False
        # Do not accept ties

        if not abs(self.scoreA.data - self.scoreB.data) >= 2:
            ok = False
        # Must win by 2

        if self.playerA.data == self.playerB.data:
            ok = False
        # Cannot play against yourself

        return ok
