import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from telepyrobot import (
    COMMAND_HAND_LER,
    LOGGER,
    OWNER_ID,
    PM_PERMIT,
    PRIVATE_GROUP_ID,
    OWNER_NAME,
)
from telepyrobot.utils.parser import mention_markdown
from telepyrobot.utils.sql_helpers import pmpermit_db as db
from telepyrobot.utils.cust_p_filters import sudo_filter
from telepyrobot.utils.pyrohelpers import extract_user

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Annoyed from People sending you private messages? :v
Here is the solution, whenever people text you, It'll show them
a message that you are not available

`{COMMAND_HAND_LER}pm`: To allow a user to pm you!
`{COMMAND_HAND_LER}dispm`: To disallow a user to pm you!
"""

DEFAULT_USER = str(OWNER_NAME) if OWNER_NAME else "Set `OWNER_NAME` in Config Vars"

welc_txt = f"""
**__Hello! This is__** @TelePyroBot
`Private Messaging Security Protocol ⚠️`
**Currently My Master** {DEFAULT_USER} **is busy!**
__Better not spam his Inbox!__
"""


@Client.on_message(filters.private & (~filters.me & ~filters.bot), group=3)
async def pm_block(c: Client, m: Message):
    if not PM_PERMIT:
        return
    try:
        if not db.get_whitelist(message.chat.id):
            if db.get_msg_id(message.chat.id):
                old_msg_id = db.get_msg_id(message.chat.id)
                await client.delete_messages(
                    chat_id=message.chat.id, message_ids=old_msg_id
                )

            rply_msg = await m.reply_text(welc_txt)
            db.set_last_msg_id(message.chat.id, rply_msg.message_id)
            await asyncio.sleep(2)
            await c.send_message(
                PRIVATE_GROUP_ID,
                "{} **wants to contact you in PM**".format(
                    mention_markdown(message.from_user.first_name, m.from_user.id)
                ),
            )
            return
    except Exception as ef:
        print("Error!\n\n", ef)
        return


@Client.on_message(
    filters.me & filters.command(["approve", "pm"], COMMAND_HAND_LER) & filters.private
)
async def approve_pm(c: Client, m: Message):
    if message.chat.type == "private":
        user_id = message.chat.id
    else:
        user_id, user_first_name = extract_user(message)
    db.set_whitelist(user_id, True)
    user = await client.get_users(user_id)
    await m.edit(
        "**__PM permission was approved__** for {}".format(
            mention_markdown(user.first_name, user_id)
        )
    )
    if db.get_msg_id(message.chat.id):
        old_msg_id = db.get_msg_id(message.chat.id)
        await client.delete_messages(chat_id=message.chat.id, message_ids=old_msg_id)
    await c.send_message(
        PRIVATE_GROUP_ID,
        "{} **is approved to contact you in PM!**".format(
            mention_markdown(user.first_name, user_id)
        ),
    )
    await asyncio.sleep(5)
    await m.delete()


@Client.on_message(
    filters.me
    & filters.command(["revoke", "disapprove", "dispm"], COMMAND_HAND_LER)
    & filters.private
)
async def revoke_pm_block(c: Client, m: Message):
    if message.chat.type == "private":
        user_id = message.chat.id
    else:
        user_id = message.text.split(" ")[1]
    db.del_whitelist(user_id)
    user = await client.get_users(user_id)
    await m.edit(
        "__**PM permission was revoked for**__ {}".format(
            mention_markdown(user.first_name, user_id)
        )
    )
    user_id = message.chat.id
    await c.send_message(
        PRIVATE_GROUP_ID,
        "{}'s **permission to contact you in PM has been revoked!**".format(
            mention_markdown(user.first_name, user_id)
        ),
    )
    await asyncio.sleep(5)
    await m.delete()
