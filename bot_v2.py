# New advanced version
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

async def ai_reply(text):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            max_tokens=50
        )
        return res.choices[0].message.content.strip()
    except:
        return "AI error 😅"

@dp.message_handler()
async def handle_message(message: types.Message):
    text = message.text.lower()

    if "ai" in text or "help" in text:
        await asyncio.sleep(2)
        reply = await ai_reply(message.text)
        await message.reply(reply)

    if message.reply_to_message and message.from_user.id == ADMIN_ID:
        if "mute" in text:
            user_id = message.reply_to_message.from_user.id
            keyboard = InlineKeyboardMarkup()
            keyboard.add(
                InlineKeyboardButton("✅ Confirm", callback_data=f"mute:{user_id}"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel")
            )
            await message.reply(f"User {user_id} ko mute karna hai?", reply_markup=keyboard)

@dp.callback_query_handler()
async def callbacks(call: types.CallbackQuery):
    data = call.data

    if data.startswith("mute:"):
        user_id = int(data.split(":")[1])
        await call.message.edit_text(f"User {user_id} mute (demo) ✅")

    if data == "cancel":
        await call.message.edit_text("Action cancel ❌")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
