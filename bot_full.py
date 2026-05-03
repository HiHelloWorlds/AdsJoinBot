import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv
import openai

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

warnings = {}

async def ai_reply(text):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            max_tokens=60
        )
        return res.choices[0].message.content.strip()
    except:
        return "AI error 😅"

@dp.message_handler()
async def handle_message(message: types.Message):
    text = message.text.lower()

    # AI reply system
    if any(x in text for x in ["ai","help","bot"]):
        await asyncio.sleep(2)
        reply = await ai_reply(message.text)
        await message.reply(reply)

    # Toxic detection
    if any(x in text for x in ["gali","madarchod","bc","mc"]):
        await message.reply("⚠️ Please avoid abusive language")

    # Admin reply commands
    if message.reply_to_message and message.from_user.id == ADMIN_ID:
        user_id = message.reply_to_message.from_user.id

        if "mute" in text:
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("✅ Confirm", callback_data=f"mute:{user_id}"), InlineKeyboardButton("❌ Cancel", callback_data="cancel"))
            await message.reply(f"Mute user {user_id}?", reply_markup=kb)

        if "ban" in text:
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("✅ Confirm", callback_data=f"ban:{user_id}"), InlineKeyboardButton("❌ Cancel", callback_data="cancel"))
            await message.reply(f"Ban user {user_id}?", reply_markup=kb)

        if "warn" in text:
            warnings[user_id] = warnings.get(user_id,0)+1
            await message.reply(f"User warned ⚠️ Total: {warnings[user_id]}")

@dp.callback_query_handler()
async def callbacks(call: types.CallbackQuery):
    data = call.data

    if data.startswith("mute:"):
        uid = int(data.split(":")[1])
        try:
            await bot.restrict_chat_member(call.message.chat.id, uid, types.ChatPermissions(can_send_messages=False))
            await call.message.edit_text("User muted ✅")
        except:
            await call.message.edit_text("Mute failed ❌")

    elif data.startswith("ban:"):
        uid = int(data.split(":")[1])
        try:
            await bot.kick_chat_member(call.message.chat.id, uid)
            await call.message.edit_text("User banned 🚫")
        except:
            await call.message.edit_text("Ban failed ❌")

    elif data == "cancel":
        await call.message.edit_text("Cancelled ❌")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
