# Lots of lub to @r4v4n4 for gibing the base <3
import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.events import register
from userbot import bot, CMD_HELP

@register(outgoing=True, disable_errors=True, pattern="^!scan(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("```javes: Can't scan bot meaage```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("```javes: reply to a media message```")
       return
    chat = "@DrWebBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("```javes: Reply to actual users message.```")
       return
    await event.edit(" `javes: Scanning......`")
    async with bot.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=161163358))
              await bot.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock @sangmatainfo_bot and try again```")
              return
          if response.text.startswith("Forward"):
             await event.edit("```javes: This user have forward privacy```")
          else:
          	if response.text.startswith("Select"):
          		await event.edit("`javes: Please go to` @DrWebBot `and select your language.`") 
          	else: 
          			await event.edit(f"javes: Antivirus scan was completed. \n {response.message.message}")
