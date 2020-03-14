# For @Unibot
# (c) Shrimadhav U K
"""Auto Profile Updation Commands
.autopp"""
import asyncio
import time
from telethon import functions
from telethon.errors.rpcerrorlist import FloodWaitError
from userbot.events import register


DEL_TIME_OUT = 70


@register(outgoing=True, pattern="^.auto")
async def _(event):
    if event.fwd_from:
        return
    while True:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio = f"Iam warking for you 24hours.......now time {HM} UTC :p"
        logger.info(bio)
        try:
            await bot(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                about=bio
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        # else:
            # logger.info(r.stringify())
            # await bot.send_message(  # pylint:disable=E0602
            #     Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
            #     "Changed Profile Picture"
            # )
        await asyncio.sleep(DEL_TIME_OUT)

