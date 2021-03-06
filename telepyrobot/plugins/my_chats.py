import os

from pyrogram import filters
from pyrogram.types import Message

from telepyrobot import COMMAND_HAND_LER
from telepyrobot.__main__ import TelePyroBot
from telepyrobot.db import my_chats_db as db
from telepyrobot.utils.admin_check import admin_check

MESSAGE_RECOUNTER = 0

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))
__help__ = f"""
This module is to manage your chats, when message was received from unknown chat, and that chat was not in database, then save that chat info to your database.
**Export chats:**
`{COMMAND_HAND_LER}chatlist`: Exports the chats which you have joined!

Send your chatlist to your saved messages.
"""


def get_msgc():
    return MESSAGE_RECOUNTER


@TelePyroBot.on_message(filters.group, group=10)
async def updatemychats(c: TelePyroBot, m: Message):
    global MESSAGE_RECOUNTER, ADMIN_RECOUNTER
    db.update_chat(m.chat)
    MESSAGE_RECOUNTER += 1
    return


@TelePyroBot.on_message(filters.me &
                        filters.command("chatlist", COMMAND_HAND_LER))
async def get_chat(c: TelePyroBot, m: Message):
    await m.edit("`Exporting Chatlist...`")
    all_chats = db.get_all_chats()
    chatfile = "<---List of chats that you joined--->\n\n"
    u = 0
    for chat in all_chats:
        u += 1
        if str(chat.chat_username) != "None":
            chatfile += "[{}] {} - ({}): @{}\n".format(
                u, chat.chat_name, chat.chat_id, chat.chat_username
            )
        else:
            chatfile += "[{}] {} - ({})\n".format(u,
                                                  chat.chat_name, chat.chat_id)
    chatlist_file = "telepyrobot/cache/chatlist.txt"
    with open(chatlist_file, "w", encoding="utf-8") as f:
        f.write(str(chatfile))
        f.close()

    await c.send_document(
        "self", document=chatlist_file, caption="Here is the chat list that you joined."
    )
    await m.edit("`Chat list exported to saved messages.`")
    os.remove(chatlist_file)
    return
