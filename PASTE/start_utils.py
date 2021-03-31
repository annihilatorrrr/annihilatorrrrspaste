from traceback import format_exc
from pyrogram import Client
from pyrogram.errors import RPCError
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from SaitamaRobot import LOGGER, pbot
#from alita.database.chats_db import Chats
from SaitamaRobot.database.notes_db import Notes
from SaitamaRobot.database.rules_db import Rules
from SaitamaRobot.database.chats_db import Chats
from SaitamaRobot.utils.cmd_senders import send_cmd
from SaitamaRobot.utils.msg_types import Types
from SaitamaRobot.utils.string import build_keyboard, parse_button

# Initialize
rules_db = Rules()
notes_db = Notes()
chats_db = Chats()


async def get_private_note(c: Client, m: Message, help_option: str):
    """Get the note in pm of user, with parsing enabled."""
    from SaitamaRobot import BOT_USERNAME

    help_lst = help_option.split("_")
    chat_id = int(help_lst[1])

    if len(help_lst) == 2:
        all_notes = notes_db.get_all_notes(chat_id)
        chat_title = chats_db.get_chat_info(chat_id)["chat_name"]
        rply = f"Notes in {chat_title}:\n\n"
        for note in all_notes:
            note_name = note[0]
            note_hash = note[1]
            rply += f"- [{note_name}](https://t.me/{BOT_USERNAME}?start=note_{chat_id}_{note_hash})\n"
        rply += "You can retrieve these notes by tapping on the notename."
        await m.reply_text(rply, disable_web_page_preview=True, quote=True)
        return

    if len(help_lst) == 3:
        note_hash = help_option.split("_")[2]
        getnotes = notes_db.get_note_by_hash(note_hash)
    else:
        return

    if not getnotes:
        await m.reply_text("Note does not exist", quote=True)
        return

    msgtype = getnotes["msgtype"]
    if not msgtype:
        await m.reply_text(
            "<b>Error:</b> Cannot find a type for this note!!",
            quote=True,
        )
        return

    if msgtype == Types.TEXT:
        teks, button = await parse_button(getnotes["note_value"])
        button = await build_keyboard(button)
        button = InlineKeyboardMarkup(button) if button else None
        if button:
            try:
                await m.reply_text(
                    teks,
                    reply_markup=button,
                    disable_web_page_preview=True,
                    quote=True,
                )
                return
            except RPCError as ef:
                await m.reply_text(
                    "An error has occured! Cannot parse note.",
                    quote=True,
                )
                LOGGER.error(ef)
                LOGGER.error(format_exc())
                return
        else:
            await m.reply_text(teks, quote=True, disable_web_page_preview=True)
            return
    elif msgtype in (
        Types.STICKER,
        Types.VIDEO_NOTE,
        Types.CONTACT,
        Types.ANIMATED_STICKER,
    ):
        await (await send_cmd(c, msgtype))(m.chat.id, getnotes["fileid"])
    else:
        if getnotes["note_value"]:
            teks, button = await parse_button(getnotes["note_value"])
            button = await build_keyboard(button)
            button = InlineKeyboardMarkup(button) if button else None
        else:
            teks = ""
            button = None
        if button:
            try:
                await (await send_cmd(c, msgtype))(
                    m.chat.id,
                    getnotes["fileid"],
                    caption=teks,
                    reply_markup=button,
                )
                return
            except RPCError as ef:
                await m.reply_text(
                    teks,
                    quote=True,
                    reply_markup=button,
                    disable_web_page_preview=True,
                )
                LOGGER.error(ef)
                LOGGER.error(format_exc())
                return
        else:
            await (await send_cmd(c, msgtype))(
                m.chat.id,
                getnotes["fileid"],
                caption=teks,
            )
    #LOGGER.info(
   #     f"{m.from_user.id} fetched privatenote {note_hash} (type - {getnotes}) in {m.chat.id}",
 #   )
    return


async def get_private_rules(_, m: Message, help_option: str):
    chat_id = int(help_option.split("_")[1])
    rules = rules_db.get_rules(chat_id)
    chat_title = chats_db.get_chat_info(chat_id)["chat_name"]
    await m.reply_text(f"Rules for {chat_title}: {rules}",
        quote=True,
        disable_web_page_preview=True,
    )
    return
