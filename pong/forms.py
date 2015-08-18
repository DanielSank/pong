import wtforms as wtf
import wtforms.validators as validators


class AddUser(wtf.Form):
    username = wtf.StringField('Username', [validators.Length(min=4, max=12)])


class AddGame(wtf.Form):

    def __init__(self, formdata=None, players=None):
        super(AddGame, self).__init__(formdata=formdata)
        self.winner.choices = [(p, p) for p in players]
        self.loser.choices = [(p, p) for p in players]

    winner = wtf.SelectField()
    loser = wtf.SelectField()

    winner_score = wtf.IntegerField()
    loser_score = wtf.IntegerField()

    def validate(self):
        """Override default validation, checking for sensible game results."""
        if not wtf.Form.validate(self):
            return False

        ok = True

        if self.winner_score.data == self.loser_score.data:
            ok = False
        # Do not accept ties

        if not self.winner_score.data - self.loser_score.data >= 2:
            ok = False
        # Must win by at least 2

        if self.winner_score.data > 21:
            if self.winner_score.data - self.loser_score.data != 2:
                ok = False
        # If the game went over 21 then it must have been a win by exactly 2.

        if self.loser.data == self.winner.data:
            ok = False
        # Cannot play against yourself

        return ok
