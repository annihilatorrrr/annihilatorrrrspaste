# Jigarvarma2005

from datetime import datetime
from typing import List
from gtts import gTTS
import time
from pyrogram import filters
from pyrogram.types import User, Message
from bot import jigar, BOT_UNAME
import re


@jigar.on_message(filters.command(["tts",f"tts@{BOT_UNAME}"]) & ~filters.edited)
async def tts(bot, message):
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    filename = datetime.now().strftime("%d%m%y-%H%M%S%f")
    if message.reply_to_message:
        reply = message.reply_to_message.text
    elif message:
        try:
            reply = message.text.split(" ", 1)[1]
        except:
            reply = "Thanks, your self"
    # remove emojis from text
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    reply = re.sub(emoj, '', reply)
    msg_id = message.message_id
    # enable this if you want to reply to the replied msg
    """
    if message.reply_to_message:
        msg_id = message.reply_to_message.message_id
    """
    await bot.send_chat_action(message.chat.id, "record_audio")
    lang="ml"
    tts = gTTS(reply, lang)
    tts.save(f"tts-{message.from_user.id}.mp3")
    with open(f"tts-{message.from_user.id}.mp3", "rb") as f:
        linelist = list(f)
        linecount = len(linelist)
    if linecount == 1:
        await bot.send_chat_action(message.chat.id, "record_audio")
        lang = "en"
        tts = gTTS(reply, lang)
        tts.save(f"tts-{message.from_user.id}.mp3")
    with open(f"tts-{message.from_user.id}.mp3", "rb") as speech:
        await bot.send_voice(chat_id=message.chat.id, voice=speech, reply_to_message_id=msg_id)
