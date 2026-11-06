import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from fastapi import FastAPI, Request
import uvicorn

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/bot/{TOKEN}"
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "")
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(lambda message: message.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("Ассаламу алейкум! Sadaqa боты сәтті қосылды және жұмыс істеп тұр.")

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    if RENDER_EXTERNAL_URL:
        await bot.set_webhook(url=WEBHOOK_URL)
        print(f"Webhook орнатылды: {WEBHOOK_URL}")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()

@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    json_data = await request.json()
    update = Update.model_validate(json_data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"status": "ok"}

@app.get("/")
async def index():
    return {"status": "active", "message": "Bot is alive and running 24/7!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)