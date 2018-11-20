# =============================================================================
# Author: falseuser
# File Name: database.py
# Created Time: 2018-10-24 16:58:58
# Last modified: 2018-11-20 17:01:00
# Description:
# =============================================================================
import datetime
import json
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, CHAR, DATETIME, TEXT, VARCHAR
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
else:
    controller_logger.error("Unsupported Database {0}".format(DB_TYPE))

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Config(Base):

    __tablename__ = "Config"
    name = Column(VARCHAR(20), primary_key=True)
    content = Column(TEXT, nullable=False)  # josn string.


class Worker(Base):

    __tablename__ = "Worker"
    worker_id = Column(VARCHAR(20), primary_key=True)
    description = Column(TEXT, nullable=False)
    supported_commands = Column(TEXT, nullable=False)
    last_response_time = Column(DATETIME, nullable=False)
    online = Column(CHAR(1), nullable=False)  # Y or N
    unregistered = Column(CHAR(1), nullable=False)  # Y or N


class WorkerData(Base):
    __tablename__ = "WorkerData"
    id = Column(Integer, primary_key=True)
    worker_id = Column(VARCHAR(20), nullable=False)
    time = Column(DATETIME, nullable=False)
    cmd = Column(VARCHAR(50), nullable=False)
    data = Column(TEXT, nullable=False)


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
        msg = "worker {0} has been registered.".format(worker_id)
        self.commit(msg)

    def remove_worker(self, worker_id):
        worker = self.session.query(Worker).get(worker_id)
        self.session.delete(worker)
        msg = "Worker {0} has been Deleted.".format(worker_id)
        self.commit(msg)

    def get_worker(self, worker_id):
        worker = self.session.query(Worker).get(worker_id)
        return worker

    def set_worker_description(self, worker_id, description):
        worker = self.session.query(Worker).get(worker_id)
        worker.description = description
        msg = "Worker {0} description updated.".format(worker_id)
        self.commit(msg)

    def set_worker_last_response_time(self, worker_id, last_response_time):
        worker = self.session.query(Worker).get(worker_id)
        worker.last_response_time = last_response_time
        msg = "Worker {0} last response time updated.".format(worker_id)
        self.commit(msg)

    def set_worker_online(self, worker_id, online):
        worker = self.session.query(Worker).get(worker_id)
        worker.online = online
        msg = "Worker {0} online status updated.".format(worker_id)
        self.commit(msg)

    def set_worker_unregistered(self, worker_id, unregistered):
        worker = self.session.query(Worker).get(worker_id)
        worker.unregistered = unregistered
        msg = "Worker {0} has been unregistered".format(worker_id)
        self.commit(msg)

    def get_workers_count(self):
        count = self.session.query(Worker.worker_id).count()
        return count

    def get_online_workers_id(self):
        workers = self.session.query(Worker).filter(Worker.online == "Y")
        return [worker.worker_id for worker in workers]

    def get_online_workers_count(self):
        workers = self.session.query(Worker)
        count = workers.filter(Worker.online == "Y").count()
        return count

    def get_registered_workers_id(self):
        workers = self.session.query(Worker).filter(Worker.unregistered == "N")
        return [worker.worker_id for worker in workers]

    def get_registered_workers_count(self):
        workers = self.session.query(Worker)
        count = workers.filter(Worker.unregistered == "N").count()
        return count

    def add_global_config(self):
        global_config = self.session.query(Config).get("global_config")
        if not global_config:
            global_config = Config(name="global_config", content="{}")
            self.session.add(global_config)
            msg = "Initialization global config succeeded."
            self.commit(msg)

    def get_global_config_content(self):
        global_config = self.session.query(Config).get("global_config")
        return global_config.content

    def set_global_config_content(self, content):
        global_config = self.session.query(Config).get("global_config")
        global_config.content = content
        msg = "Global config content updated."
        self.commit(msg)

    def add_worker_config(self, worker_id):
        config_name = "{0}_config".format(worker_id)
        worker_config = self.session.query(Config).get(config_name)
        if not worker_config:
            worker_config = Config(name=config_name, content="{}")
            self.session.add(worker_config)
            msg = "Add worker config {0} succeeded.".format(worker_id)
            self.commit(msg)

    def get_worker_config_content(self, worker_id):
        config_name = "{0}_config".format(worker_id)
        worker_config = self.session.query(Config).get(config_name)
        return worker_config.content

    def set_worker_config_content(self, worker_id, content):
        config_name = "{0}_config".format(worker_id)
        worker_config = self.session.query(Config).get(config_name)
        worker_config.content = content
        msg = "Worker config {0} updated.".format(worker_id)
        self.commit(msg)

    def get_worker_data(self, worker_id, cmd, time_limit):
        now = datetime.datetime.now()
        if time_limit == "last":
            data = self.session.query(WorkerData).filter(
                and_(WorkerData.worker_id == worker_id, WorkerData.cmd == cmd)
            ).order_by(WorkerData.time).last()
        elif time_limit == "24h":
            start_time = now - 24
            data = self.session.query(WorkerData).filter(
                and_(
                    WorkerData.worker_id == worker_id,
                    WorkerData.cmd == cmd,
                    WorkerData.time >= start_time,
                )
            ).order_by(WorkerData.time).all()
        elif time_limit == "7d":
            pass
        return data

    def save_worker_data(self, worker_id, cmd, data):
        """Save worker returned data
        data type:
            worker_id: string
            cmd: string
            data: string
        """
        now = datetime.datetime.now()
        worker_data = WorkerData(
            worker_id=worker_id,
            time=now,
            cmd=cmd,
            data=data,
        )
        self.session.add(worker_data)
        msg = "Add worker data {0} succeeded.".format(worker_id)
        self.commit(msg)

    def commit(self, msg):
        try:
            self.session.commit()
            controller_logger.info(msg)
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
    print(dbop.get_registered_workers_count())
    dbop.close()
