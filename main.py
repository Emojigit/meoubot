#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
exit = sys.exit

try:
    import config
except ImportError:
    print("config.py not found, copying one for you...")
    import shutil
    try:
        shutil.copyfile("config.example.py","config.py")
        print("Config file copied, follow the instructions inside to config the bot.")
    except FileNotFoundError:
        print("config.example.py not found, make sure you're in the script's directory!")
    exit(1)

import asyncio, random, time, logging
from telethon import TelegramClient, functions, types, events
from telethon.errors import *

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s[%(name)s]: %(message)s")

log = logging.getLogger()

def meougen():
    return ("喵" * random.randint(3, 5)) + "～"

bot = TelegramClient('bot', config.api_id, config.api_hash).start(bot_token=config.bot_token)
client = bot

rlimit = {}

@bot.on(events.NewMessage)
async def msg(event):
    now = time.time()
    if event.sender_id in rlimit:
        if now - rlimit[event.sender_id] < config.rlimit:
            if event.is_private:
                await event.respond("太快了喵！")
                return
    rlimit[event.sender_id] = now
    text = event.message.text
    if (text.startswith("/start") or text.startswith("/help")) and event.is_private:
        await event.respond("私聊發送任何信息我會喵喵～\n群組發送喵叫信息我會喵喵～\n我們不會留下喵喵記錄污染貓糧哦喵～")
    if event.is_private or ("喵" in text) or text.startswith("/meou"):
        await (event.respond if event.is_private else event.reply)(meougen())

@bot.on(events.InlineQuery)
async def inline(event):
    now = time.time()
    if event.sender_id in rlimit:
        if now - rlimit[event.sender_id] < config.rlimit:
            await event.answer([
                event.builder.article("太快了喵！", text="太快了喵！"),
            ])
            return
    rlimit[event.sender_id] = now
    msg = meougen()
    await event.answer([
        event.builder.article(msg, text=msg),
    ])

@bot.on(events.NewMessage(pattern="/meouleave"))
async def msg(event):
    if event.sender.id == config.owner:
        await bot.kick_participant(event.chat, 'me')

bot.run_until_disconnected()

