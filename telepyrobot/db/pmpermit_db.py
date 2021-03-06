import threading

from sqlalchemy import Column, Integer, String

from telepyrobot.db import BASE, SESSION


class PMTable(BASE):
    __tablename__ = "pmapprove"
    user_id = Column(Integer, primary_key=True)
    boolvalue = Column(String)

    def __init__(self, user_id, boolvalue):
        self.user_id = user_id
        self.boolvalue = boolvalue


class MsgID(BASE):
    __tablename__ = "msgid_pm"
    user_id = Column(Integer, primary_key=True)
    msg_id = Column(Integer)

    def __init__(self, user_id, msg_id):
        self.user_id = user_id
        self.msg_id = msg_id


PMTable.__table__.create(checkfirst=True)
MsgID.__table__.create(checkfirst=True)


INSERTION_LOCK = threading.RLock()


def set_whitelist(user_id, boolvalue):
    with INSERTION_LOCK:
        user = SESSION.query(PMTable).get(user_id)
        try:
            if not user:
                user = PMTable(user_id, boolvalue)
            else:
                user.boolvalue = str(boolvalue)
            SESSION.add(user)
            SESSION.commit()
        finally:
            SESSION.close()
    return user_id


def set_last_msg_id(user_id, msg_id):
    with INSERTION_LOCK:
        try:
            user = SESSION.query(MsgID).get(user_id)
            if not user:
                user = MsgID(user_id, msg_id)
            else:
                user.msg_id = msg_id
            SESSION.merge(user)
            SESSION.commit()
        finally:
            SESSION.close()


def get_msg_id(user_id):
    try:
        user = SESSION.query(MsgID).get(user_id)
        msg_id = None
        if user:
            msg_id = user.msg_id
            return msg_id
    finally:
        SESSION.close()


def del_whitelist(user_id):
    with INSERTION_LOCK:
        user = SESSION.query(PMTable).get(user_id)
        try:
            if user:
                SESSION.delete(user)
                SESSION.commit()
        finally:
            SESSION.close()
        return False


def get_whitelist(user_id):
    user = SESSION.query(PMTable).get(user_id)
    rep = ""
    if user:
        rep = str(user.boolvalue)
    SESSION.close()
    return rep
