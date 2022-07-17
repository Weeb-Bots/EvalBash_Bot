# Bot By Kai84'
import uvloop
import os
import time
import asyncio
import io
import shutil
import sys
import time
import traceback
import logging

from pyrogram import Client, filters
from Config import Config
from pyrogram.types import Message
from logging.handlers import RotatingFileHandler
from subprocess import check_output, STDOUT
from telegraph import Telegraph

uvloop.install()

USR = Config.USERS.split(" ") if " " in Config.USERS else int(Config.USERS)
app = Client("Kai84",
         API_ID = Config.TGID,
         API_HASH = Config.TGHASH,
         BOT_TOKEN = Config.BOT_TOKEN
       )
prefixes = ["/",".","-","#","~"]
MAX_MESSAGE_LENGTH = 4096
FREE_USER_MAX_FILE_SIZE = 2097152000
telegraph = Telegraph()
telegraph.create_account(short_name='Kai84', author_name="Keqing Izuka")

@app.on_message(filters.user(USR) & filters.coomand("pip", prefixes=prefixes)
async def bash_cmd(m: Message, bot):
  text = m.text
  if m.text is None:
     return m.reply_text("Send A Pypi File to Get Loaded in The System", quote=True)
  else:
     text = str(text.split(" ", 1)[-1])
  try:
    reply_t = check_output(["pip3", "install", "-U", text], stderr=STDOUT, shell=True, encoding="utf-8")
  except Exception as r:
    return m.reply_text(f"Error:\n\n{str(r)}", quote=True)
  help = telegraph.create_page(
        title='Sword Torrentz Mirror Help',
        content=str(reply_t),
    )["path"]
  await m.reply_text(f"Successfully Installed [{text}](https://telegra.ph/{help})")

async def eval(filters.user(USR) & filters.coomand("eval", prefixes=prefixes):
    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]
    reply_to_id = message.id
    if message.reply_to_message:
      reply_to_id = message.reply_to_message.id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
  
    try:
      await aexec(cmd, bot, message)
    except Exception:
      exc = traceback.format_exc()
        
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
  
    evaluation = ""
    if exc:
      evaluation = exc
    elif stderr:
      evaluation = stderr
    elif stdout:
      evaluation = stdout
    else:
      evaluation = "Success"
  
    final_output = (
      "<b>EVAL</b>: <code>{}</code>\n\n<b>OUTPUT</b>:\n<code>{}</code> \n".format(
        cmd, evaluation.strip()
      )
    )

    if len(final_output) > MAX_MESSAGE_LENGTH:
      with open("eval.txt", "w+", encoding="utf8") as out_file:
        out_file.trunicate(0)
        out_file.write(str(final_output))
        await message.reply_document(
          document="eval.txt",
          caption=cmd,
          disable_notification=True,
          reply_to_message_id=reply_to_id,
        )
        os.remove("eval.txt")
        await status_message.delete()
    else:
      await status_message.edit(final_output)
