# =============================================================================
# Author: falseuser
# File Name: database.py
# Created Time: 2018-10-24 16:58:58
# Last modified: 2018-10-24 18:29:07
# Description:
# =============================================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Integer, Unicode, DateTime
from controller_utils import config


DB_TYPE = config.get('database', 'db_type')
DB_NAME = config.get('database', 'db_name')

if DB_TYPE == "sqlite":
    DB_FILE = config.get('sqlite', 'db_file')
    engine = create_engine("sqlite://{0}".format(DB_FILE))

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Config(Base):

    __tablename__ = "Config"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True, index=True)
    content = Column(Unicode(1024), nullable=False)  # josn string.

    def __repr__(self):
        return "<Config>{0}:{1}".format(self.id, self.name)


class Worker(Base):

    __tablename__ = "Worker"
    id = Column(Integer, primary_key=True)
    worker_id = Column(String(20), nullable=False, unique=True, index=True)
    description = Column(Unicode(1024), nullable=False)
    supported_commands = Column(Unicode(1024), nullable=False)
    last_response_time = Column(DateTime, nullable=False)
    online = Column(String(1), nullable=False)  # Y or N
    unregistered = Column(String(1), nullable=False)  # Y or N

    def __repr__(self):
        return "<Config>{0}:{1}".format(self.id, self.worker_id)


Base.metadata.create_all(engine)
session = Session()
session.commit()
session.rollback()
session.close()


class DBOperation(object):
    pass
