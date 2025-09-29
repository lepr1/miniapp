import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import Command
import keyboards as kb
from config import WEBAPP_URL

router = Router()

# клавиатура для WebApp
main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🚀 Открыть сайт", web_app=WebAppInfo(url=WEBAPP_URL))]],
    resize_keyboard=True
)

# /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Нажми кнопку, чтобы открыть WebApp и заказать шмотки:",
        reply_markup=main_kb
    )

# обработка web_app_data
@router.message()
async def handle_webapp(message: Message):
    if message.web_app_data:
        raw = message.web_app_data.data
        try:
            payload = json.loads(raw)
            username = payload.get("username", "—")
            size = payload.get("size", "—")
            item = payload.get("item", "—")
            count = payload.get("count", "—")
            delivery = payload.get("delivery", "—")
            metro = payload.get("metro", "—")

            metro_text = "—" if delivery == "pickup" else metro

            text = (
                "<b>Новый заказ из WebApp</b>\n\n"
                f"Username: {username}\n"
                f"Размер: {size}\n"
                f"Товар: {item}\n"
                f"Количество: {count}\n"
                f"Доставка: {delivery}\n"
                f"Метро: {metro_text}\n\n"
                f"Проверьте правильность заказа и подтвердите (отмените) заказ 🔽"


            )
            await message.answer(text, reply_markup=kb.confirm_order,parse_mode="HTML")

        except Exception:
            await message.answer(f"Данные с WebApp: {raw}")

@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery):
    await callback.bot.send_message(chat_id="", text=callback.message.text)
    await callback.message.edit_text(callback.message.text + "\n\n✅ Заказ подтверждён", reply_markup=None)

# Отменить заказ
@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery):
    await callback.message.delete()
