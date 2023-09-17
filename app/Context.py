import os
import mysql.connector
from sqlalchemy import create_engine, text, func, or_
from sqlalchemy.orm import sessionmaker
from app.util.DotDict import DotDict

# models
from app.model.base import Base
from app.model.channel import Channel
from app.model.setting import Setting
from app.model.message import Message
from app.model.history import history
from collections.abc import Iterable

from app.config.config import Config


class Context:
    def __init__(self):
        db_name = Config.database_name
        db_user = Config.database_user
        db_pass = Config.database_pass
        db_host = Config.database_host
        db_port = Config.database_port
        db_url = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(db_url, isolation_level="AUTOCOMMIT")
        Base.metadata.create_all(self.engine)

    def _session(self):
        Session = sessionmaker(bind=self.engine,)
        return Session()

    def _exec(self, query, session=None):
        new_session = None
        try:
            if session:
                if not session.is_active:
                    session.begin()
                result = query(session)
                return result
            else:
                new_session = self._session()
                if not new_session.is_active:
                    with new_session.begin() as transaction:
                        result = query(new_session)
                else:
                    result = query(new_session)

                if new_session.dirty:
                    new_session.commit()
                new_session.close()
                return result

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            if new_session:
                new_session.rollback()
                new_session.close()
            raise e

    # channel
    def get_all_channel(self, session=None):
        return self._exec(
            lambda sess: sess.query(Channel)
            .filter(Channel.deleted_at == None)
            .all(), session)

    def count_channels(self, session=None):
        return self._exec(
            lambda sess: sess.query(func.count(Channel.id))
            .filter(Channel.deleted_at == None)
            .scalar(), session)

    def add_channel(self, session=None):
        pass

    def edit_channel(self, session=None):
        pass

    def delete_channel(self, session=None):
        pass

    # message
    def get_all_message(self, session=None):
        return self._exec(
            lambda sess: sess.query(Message)
            .filter(Message.deleted_at == None)
            .all(), session)

    def add_message(self, session=None):
        pass

    def edit_message(self, session=None):
        pass

    def delete_message(self, session=None):
        pass

    # history
    def add_history(self, session=None):
        pass

    # setting
    def get_setting(self, key, session=None):
        return self._exec(
            lambda sess: sess.query(Setting).filter_by(key=key).first(), session)

    def add_or_update_setting(self, key, value, session=None):
        def _f(session):
            setting = self.get_setting(key, session)
            if setting:
                setting.value = value
            else:
                new_setting = Setting(key=key, value=value)
                self.session.add(new_setting)
        return self._exec(_f, session)
