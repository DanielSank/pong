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
    playerA_name = Column(String(USER_NAME_LEN), ForeignKey('users.name'))
    playerB_name = Column(String(USER_NAME_LEN), ForeignKey('users.name'))

    playerA = relationship("User", foreign_keys=[playerA_name])
    playerB = relationship("User", foreign_keys=[playerB_name])

    scoreA = Column(Integer, nullable=False)
    scoreB = Column(Integer, nullable=False)
