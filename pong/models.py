from sqlalchemy import Column, Integer, String, ForeignKey, Date
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
    playerA = Column(String(USER_NAME_LEN), ForeignKey('users.name'))
    playerB = Column(String(USER_NAME_LEN), ForeignKey('users.name'))
    scoreA = Column(Integer, nullable=False)
    scoreB = Column(Integer, nullable=False)
