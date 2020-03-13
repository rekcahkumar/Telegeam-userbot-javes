
from telethon import events
import asyncio
from collections import deque
from userbot.events import register

@register(outgoing=True, disable_errors=True, pattern="^.load")
async def _(event):
	if event.fwd_from:
		return 
	deq = deque(list("Loading....."))
	for _ in range(1000):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(-1)
    
