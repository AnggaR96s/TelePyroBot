import asyncio
import io
import os
import sys
import time
import traceback

import requests
from pyrogram import filters
from pyrogram.types import Message

from telepyrobot import COMMAND_HAND_LER, MAX_MESSAGE_LENGTH
from telepyrobot.__main__ import TelePyroBot

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
List the directories of the server.

`{COMMAND_HAND_LER}ls`: List files in ./ directory
`{COMMAND_HAND_LER}ls <diectory name>`: List all the files in the directory.
"""


@TelePyroBot.on_message(filters.command("ls", COMMAND_HAND_LER) & filters.me)
async def list_directories(c: TelePyroBot, m: Message):
    if len(m.command) == 1:
        cmd = "ls"
    elif len(m.command) >= 2:
        location = m.text.split(" ", 1)[1]
        cmd = "ls " + location
    else:
        await m.edit(
            "<b>Error:</b>\n<i>Check Help documentaion for directory listing.</i>"
        )

    reply_to_id = m.message_id

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    OUTPUT = stdout.decode()
    if not OUTPUT:
        OUTPUT = "No Output"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with open("exec.txt", "w+", encoding="utf8") as out_file:
            out_file.write(str(OUTPUT))
        await m.reply_document(
            document="exec.txt",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove("exec.txt")
    else:
        await m.reply_text(OUTPUT)
    return
