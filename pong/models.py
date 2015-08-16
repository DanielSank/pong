from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import datetime


USER_NAME_LEN = 24


Base = declarative_base()


class User(Base):
    """A user"""

    __tablename__ = 'users'

    name = Column(String(USER_NAME_LEN), primary_key=True)


class Game(Base):
    """A game"""

    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, default=datetime.date)

    winner_name = Column(String(USER_NAME_LEN),
                         ForeignKey('users.name'),
                         nullable=False)
    loser_name = Column(String(USER_NAME_LEN),
                        ForeignKey('users.name'),
                        nullable=False)

    winner = relationship("User", foreign_keys=[winner_name])
    loser = relationship("User", foreign_keys=[loser_name])

    winner_score = Column(Integer, nullable=False)
    loser_score = Column(Integer, nullable=False)
