import logging
from aiogram import Bot, Dispatcher, executor, types
import aiohttp

API_TOKEN = '8118413772:AAHWv8upxADoM2Y2Ehs2odcWZXHVB_DZnZ0'
PEAKERR_API_KEY = 'f5b50bd9ca9352424f8d6e8b886e88f3'
ADMIN_ID = 8118413772
UPI_ID = 'Suhailmm07@ybl'
CURRENCY = 'INR'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.reply(f"👋 Welcome, {msg.from_user.first_name}!
Use /services to view options or /balance to top-up.")

@dp.message_handler(commands=['balance'])
async def balance(msg: types.Message):
    await msg.reply(f"💳 *Add Balance*
Send payment to UPI: `{UPI_ID}`
Then upload your screenshot with caption:
`Paid 100`

Admin will verify.",
                    parse_mode='Markdown')

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_payment_screenshot(msg: types.Message):
    if msg.caption and "paid" in msg.caption.lower():
        await bot.send_message(ADMIN_ID, f"📥 Payment proof from @{msg.from_user.username or msg.from_user.id}
💬 Caption: {msg.caption}")
        await msg.reply("✅ Screenshot received. Please wait for admin approval.")
    else:
        await msg.reply("❗Please upload the screenshot with a caption like: Paid 100")

@dp.message_handler(commands=['services'])
async def services(msg: types.Message):
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": PEAKERR_API_KEY}
        async with session.get("https://peakerr.com/api/v2", headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                if 'services' in data:
                    reply = "🛍 Available Services:

"
                    for srv in data['services'][:10]:
                        reply += f"• {srv['name']} (ID: {srv['service']}) — ₹{srv['rate']} per {srv['min']}–{srv['max']}
"
                    await msg.reply(reply)
                else:
                    await msg.reply("⚠️ Failed to fetch services.")
            else:
                await msg.reply("⚠️ Error contacting SMM API.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
