import asyncio
import json
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, Message
from aiogram.filters import Command
from aiogram import Router
from config import BOT_TOKEN

WEBAPP_URL = "https://3823474339f6.ngrok-free.app" 

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# клавиатура
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚀 Открыть сайт", web_app=WebAppInfo(url=WEBAPP_URL))
        ]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет, настоящий ценитель искусства!\n\n Нажми кнопку, чтобы открыть WebApp и заказать самые лучшие шмотки:", reply_markup=main_kb)

# Обработчик любых сообщений в router — мы проверяем web_app_data
@router.message()
async def handle_webapp(message: Message):
    if message.web_app_data:
        raw = message.web_app_data.data  # строка, в нашем случае JSON
        try:
            payload = json.loads(raw)
            username = payload.get("username", "—")
            size = payload.get("size", "—")
            item = payload.get("item", "—")
            count = payload.get("count", "—")

            text = (
                "<b>Новый заказ из WebApp</b>\n\n"
                f"Username: {username}\n"
                f"Размер: {size}\n"
                f"Товар: {item}\n"
                f"Количество: {count}"
            )
            await message.answer(text, parse_mode="HTML")
        except Exception as e:
            # Если не JSON — просто отправим сырой текст
            await message.answer(f"Данные с WebApp: {raw}")
    # если message.web_app_data нет — ничего не делаем (или можно обработать текстовые сообщения)


dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
