"""
BSD 2-Clause License
Copyright (C) 2017-2019, Paul Larsen
Copyright (C) 2022-2023, Awesome-Prince, [ https://github.com/Awesome-Prince]
Copyright (c) 2022-2023,Programmer Network, [ https://github.com/Awesome-Prince/NekoRobot-3 ]
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import threading

from sqlalchemy import BigInteger, Boolean, Column, String

from NekoRobot.modules.sql import BASE, SESSION


class SPinSettings(BASE):
    __tablename__ = "pin_settings"

    chat_id = Column(String(14), primary_key=True)
    message_id = Column(BigInteger)
    suacpmo = Column(Boolean, default=False)
    scldpmo = Column(Boolean, default=False)

    def __init__(self, chat_id, message_id):
        self.chat_id = str(chat_id)
        self.message_id = message_id

    def __repr__(self):
        return "<Pin Settings for {} in {}>".format(self.chat_id, self.message_id)


SPinSettings.__table__.create(checkfirst=True)

PIN_INSERTION_LOCK = threading.RLock()


def add_mid(chat_id, message_id):
    with PIN_INSERTION_LOCK:
        chat = SESSION.query(SPinSettings).get(str(chat_id))
        if not chat:
            chat = SPinSettings(str(chat_id), message_id)
        SESSION.add(chat)
        SESSION.commit()
        SESSION.close()


def remove_mid(chat_id):
    with PIN_INSERTION_LOCK:
        chat = SESSION.query(SPinSettings).get(str(chat_id))
        if chat:
            SESSION.delete(chat)
            SESSION.commit()
        SESSION.close()


def add_acp_o(chat_id, setting):
    with PIN_INSERTION_LOCK:
        chat = SESSION.query(SPinSettings).get(str(chat_id))
        if not chat:
            chat = SPinSettings(str(chat_id), 0)
        chat.suacpmo = setting
        SESSION.add(chat)
        SESSION.commit()
        SESSION.close()


def add_ldp_m(chat_id, setting):
    with PIN_INSERTION_LOCK:
        chat = SESSION.query(SPinSettings).get(str(chat_id))
        if not chat:
            chat = SPinSettings(str(chat_id), 0)
        chat.scldpmo = setting
        SESSION.add(chat)
        SESSION.commit()
        SESSION.close()


def get_current_settings(chat_id):
    with PIN_INSERTION_LOCK:
        chat = SESSION.query(SPinSettings).get(str(chat_id))
        return chat
