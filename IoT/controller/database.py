# =============================================================================
# Author: falseuser
# File Name: database.py
# Created Time: 2018-10-24 16:58:58
# Last modified: 2018-10-25 16:22:09
# Description:
# =============================================================================
import datetime
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, CHAR, DATETIME, TEXT, VARCHAR
from controller_utils import (
    config,
    BASE_COMMANDS,
    controller_logger,
    DatabaseOperationError,
)


DB_TYPE = config.get('database', 'type')
DB_NAME = config.get('database', 'db_name')

if DB_TYPE == "sqlite":
    DB_FILE = config.get('sqlite', 'db_file')
    engine = create_engine("sqlite:///{0}".format(DB_FILE))

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Config(Base):

    __tablename__ = "Config"
    name = Column(VARCHAR(20), primary_key=True)
    content = Column(TEXT, nullable=False)  # josn string.

    def __repr__(self):
        return "<Table: Config> {0}".format(self.name)


class Worker(Base):

    __tablename__ = "Worker"
    worker_id = Column(VARCHAR(20), primary_key=True)
    description = Column(TEXT, nullable=False)
    supported_commands = Column(TEXT, nullable=False)
    last_response_time = Column(DATETIME, nullable=False)
    online = Column(CHAR(1), nullable=False)  # Y or N
    unregistered = Column(CHAR(1), nullable=False)  # Y or N

    def __repr__(self):
        return "<Table: Worker> {0}".format(self.worker_id)


# Create Tables if not exist.
Base.metadata.create_all(engine)


class DBOperation(object):

    def __init__(self):
        self.session = Session()

    def add_worker(self, worker_id, description):
        now = datetime.datetime.now()
        cmds = json.dumps(BASE_COMMANDS)
        worker = Worker(
            worker_id=worker_id,
            description=description,
            supported_commands=cmds,
            last_response_time=now,
            online="Y",
            unregistered="N",
        )
        self.session.add(worker)
        self.commit()
        # add log

    def del_worker(self, worker_id):
        worker = self.session.query(Worker).get(worker_id)
        self.session.delete(worker)
        self.commit()
        # add log

    def get_worker(self, worker_id):
        worker = self.session.query(Worker).get(worker_id)
        return worker

    def set_worker_description(self, worker_id, description):
        worker = self.session.query(Worker).get(worker_id)
        worker.description = description
        self.commit()

    def set_worker_last_response_time(self, worker_id, last_response_time):
        worker = self.session.query(Worker).get(worker_id)
        worker.last_response_time = last_response_time
        self.commit()

    def set_worker_online(self, worker_id, online):
        worker = self.session.query(Worker).get(worker_id)
        worker.online = online
        self.commit()

    def set_worker_unregistered(self, worker_id, unregistered):
        worker = self.session.query(Worker).get(worker_id)
        worker.unregistered = unregistered
        self.commit()

    def add_global_config(self):
        global_config = self.session.query(Config).get("global_config")
        if not global_config:
            global_config = Config(name="global_config", content="{}")
            self.session.add(global_config)
            self.commit()

    def get_global_config_content(self):
        global_config = self.session.query(Config).get("global_config")
        return global_config.content

    def set_global_config_content(self, content):
        global_config = self.session.query(Config).get("global_config")
        global_config.content = content
        self.commit()

    def add_worker_config(self, worker_id):
        config_name = "{0}_config".format(worker_id)
        worker_config = self.session.query(Config).get(config_name)
        if not worker_config:
            worker_config = Config(name=config_name, content="{}")
            self.session.add(worker_config)
            self.commit()

    def get_worker_config_content(self, worker_id):
        config_name = "{0}_config".format(worker_id)
        worker_config = self.session.query(Config).get(config_name)
        return worker_config.content

    def set_worker_config_content(self, worker_id, content):
        config_name = "{0}_config".format(worker_id)
        worker_config = self.session.query(Config).get(config_name)
        worker_config.content = content
        self.commit()

    def commit(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            controller_logger.error("Database operation failed.")
            controller_logger.exception(e)
            raise DatabaseOperationError

    def close(self):
        self.session.close()
        del self


if __name__ == "__main__":
    dbop = DBOperation()
    dbop.add_global_config()
    try:
        dbop.add_worker("worker_1", "test worker")
    except Exception as e:
        print(e)
        worker = dbop.get_worker("worker_1")
        print(worker)
        print(worker.supported_commands)
        print(worker.last_response_time)
    dbop.close()
