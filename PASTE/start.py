from pyrogram import Client, filters
from pyrogram.errors import MessageNotModified, QueryIdInvalid, UserIsBlocked
from pyrogram.types import Message
from SaitamaRobot import pbot#, LOGGER
from SaitamaRobot.utils.custom_filters import command
from SaitamaRobot.utils.start_utils import (
    get_private_note,
    get_private_rules,
)


@pbot.on_message(
    command("start") & (filters.group | filters.private),
)
async def start(c: Client, m: Message):

    if m.chat.type == "private":
        if len(m.text.split()) > 1:
            help_option = (m.text.split(None, 1)[1]).lower()

            if help_option.startswith("note"):
                await get_private_note(c, m, help_option)
                return
            if help_option.startswith("rules"):
             #   LOGGER.info(f"{m.from_user.id} fetched privaterules in {m.chat.id}")
                await get_private_rules(c, m, help_option)
                #return
          #  return
       # except UserIsBlocked:
          #  LOGGER.warning(f"Bot blocked by {m.from_user.id}")
    return
