import os
import requests
from pyrogram import *

from config import Config
from pyrogram.types import *
from googletrans import Translator

OWNER_USERNAME = Config.OWNER_USERNAME
BOT_TOKEN = Config.BOT_TOKEN
BOT_ID = int(BOT_TOKEN.split(":")[0])
MERISSA_TOKEN = Config.MERISSA_TOKEN
BOT_NAME = Config.BOT_NAME
OWNER_NAME = Config.OWNER_NAME
LANG = Config.LANGUAGE_CODE

chatbot_group = 2

bot = Client("MerissaChatbot", bot_token=BOT_TOKEN, api_id=6,
             api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

tr = Translator()

@bot.on_message(filters.command("start") & ~filters.edited)
async def start(client, message):
   if message.chat.type == 'private':
       await message.reply(f"Saya {BOT_NAME} 😎.",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "Pemilik", url=f"https://t.me/{OWNER_USERNAME}"),
                                        InlineKeyboardButton(
                                            "Grup", url="t.me/HaoTogelLivedraw")
                                    ]]
                            ),               
           )
   else:
       await message.reply("**I'm alive, check my pm to know more about me!**")

@bot.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded
    & ~filters.edited,
    group=chatbot_group,  
)
async def chatbot_talk(_, message: Message):
    chat = message.chat.id
    if not message.reply_to_message:
        return
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id != BOT_ID:
        return
    if message.text[0] == "/":
        return
    if chat:
        await bot.send_chat_action(message.chat.id, "typing")
        lang = tr.translate(message.text).src
        trtoen = (
            message.text if lang == "id" else tr.translate(message.text, dest="id").text
        ).replace(" ", "%20")
        text = trtoen.replace(" ", "%20") if len(message.text) < 2 else trtoen
        merissaurl = requests.get(
            f"https://merissachatbot.tk/api/apikey={MERISSA_TOKEN}/{BOT_NAME}/{OWNER_NAME}/message={text}"
        )
        textmsg = merissaurl.json()["reply"]
        msg = tr.translate(textmsg, src="id", dest=LANG)
        await message.reply_text(msg.text)

print("Merissa Chatbot Started!")
bot.run()
