import os

from sqlalchemy import Table, text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Numeric
from sqlalchemy.orm import sessionmaker, relationship, object_session
from sqlalchemy.engine.url import URL

from hansard import settings

Base = declarative_base()
session = sessionmaker()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_table(engine):
    """"""
    Base.metadata.create_all(engine)

debate_mps_association = Table(
    'debate_mps', Base.metadata,
    Column('mp_id', ForeignKey('mps.id'), primary_key=True),
    Column('debate_id', ForeignKey('debates.id'), primary_key=True)
    )

class MP(Base):
    __tablename__ = 'mps'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_year = Column(Integer)
    end_year = Column(String)
    constituency_last = Column(String)
    house = Column(String)
    debates = relationship('Debate', 
                            secondary=debate_mps_association, 
                            back_populates='mps')
    #spoken_contribution_id = Column(Integer, ForeignKey('spoken_contributions.id'))
    spoken_contributions = relationship('SpokenContribution', 
                                        back_populates='mps')
    party_id = Column(Integer, ForeignKey('parties.id'))
    party = relationship("Party", back_populates='mps')

class Debate(Base):
    __tablename__ = 'debates'

    id = Column(Integer, primary_key=True)
    debate_id = Column(String)
    debate_name = Column(String)
    debate_date = Column(DateTime)
    mps = relationship("MP", 
                        secondary=debate_mps_association, 
                        back_populates="debates")
    spoken_contributions = relationship('SpokenContribution', 
                                        back_populates='debates')

class SpokenContribution(Base):
    __tablename__ = 'spoken_contributions'

    id = Column(Integer, primary_key=True)
    contribution_id = Column(String)
    text = Column(String)
    time = Column(DateTime)
    mp_id = Column(Integer, ForeignKey('mps.id'))
    mp = relationship("MP", back_populates="spoken_contributions")
    debate_id = Column(Integer, ForeignKey('debates.id'))
    debate = relationship("Debate", back_populates="spoken_contributions")

class Party(Base):
    __tablename__ = 'parties'

    id = Column(Integer, primary_key=True)
    party = Column(String)
    mps = relationship("MP", back_populates="party")


