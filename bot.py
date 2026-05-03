import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def handle_message(message: types.Message):
    text = message.text.lower()

    # Simple AI-like reply trigger
    if "ai" in text or "bot" in text:
        await message.reply("Hello 👋 main AI bot hoon, kaise help karu?")

    # Reply-based mute command (basic demo)
    if message.reply_to_message and message.from_user.id == ADMIN_ID:
        if "mute" in text:
            user_id = message.reply_to_message.from_user.id
            await message.reply(f"User {user_id} ko mute karne ka demo (real logic baad me add hoga)")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
