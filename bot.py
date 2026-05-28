import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

# ВПИШИ СВОИ ДАННЫЕ СЮДА:
BOT_TOKEN = "8737568903:AAGNyhuFcMvNO8rXfzYsiNZ-wDleLh1D_xo"
ADMIN_ID = 7812922588
GOOGLE_DRIVE_LINK = "https://drive.google.com/drive/folders/1xK-pkI95nBfEp6-iHRGiwZAn5RfRDmdy?usp=sharing"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главное меню (Клавиатура под сообщением)
def get_main_menu():
    buttons = [
        [InlineKeyboardButton(text="🎁 Бесплатный Демо-Промт", callback_data="get_demo")],
        [InlineKeyboardButton(text="🔥 КУПИТЬ ПОЛНЫЙ ПАК (100+ промтов)", callback_data="buy_pack")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура для админа (для быстрой выдачи пака)
def get_admin_keyboard(buyer_id):
    buttons = [
        [InlineKeyboardButton(text="✅ Подтвердить и выдать Пак", callback_data=f"approve_{buyer_id}")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"decline_{buyer_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Хэндлер на команду /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Ты попал в официальный бот **AI MEGA PACK 2026**.\n"
        "Здесь ты можешь получить ультимативный сборник из 100+ промтов для учебы, работы, дизайна и заработка на нейросетях.\n\n"
        "Выбери действие ниже 👇",
        reply_markup=get_main_menu()
    )

# Обработка кнопки "Бесплатный Демо-Промт"
@dp.callback_query(F.data == "get_demo")
async def process_demo(callback):
    await callback.message.answer(
        "🎁 Твой бесплатный промт для обхода Антиплагиата:\n\n"
        "`Перепиши этот текст, используя редкие синонимы и меняя структуру предложений, но полностью сохрани научный смысл. Текст должен выглядеть так, будто его написал живой студент-отличник, а не ИИ. Проверь, чтобы уникальность была выше 95%. Вот текст: [ВСТАВЬ ТЕКСТ]`\n\n"
        "*(Нажми на текст, чтобы скопировать его)*"
    )
    await callback.answer()

# Обработка кнопки "Купить полный пак"
@dp.callback_query(F.data == "buy_pack")
async def process_buy(callback):
    await callback.message.answer(
        "💸 **Оформление заказа AI MEGA PACK (100+ промтов)**\n\n"
        "Стоимость: **99 рублей** (доступ навсегда + обновления).\n\n"
        "📌 **Инструкция по оплате:**\n"
        "1. Переведи 99 руб. по СБП на номер: `+79965362676` (Ozon Банк)\n"
        "2. Получатель: Владислав Б.\n"
        "3. **ОБЯЗАТЕЛЬНО:** Сделай скриншот чека об оплате и **отправь его прямо сюда, в этот чат**.\n\n"
        "После проверки чека бот моментально пришлет тебе ссылку на весь архив!"
    )
    await callback.answer()

# Ловим скриншот чека от покупателя
@dp.message(F.photo)
async def handle_receipt(message: Message):
    # Отправляем покупателю уведомление
    await message.answer("⏳ Твой чек отправлен на проверку админу. Это займет всего пару минут, ожидай!")
    
    # Пересылаем чек админу с кнопками управления
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=f"💰 **Новый чек на проверку!**\nОт: @{message.from_user.username} (ID: {message.from_user.id})",
        reply_markup=get_admin_keyboard(message.from_user.id)
    )

# Админ нажал "Подтвердить"
@dp.callback_query(F.data.startswith("approve_"))
async def approve_payment(callback):
    buyer_id = int(callback.data.split("_")[1])
    
    # Отправляем пак покупателю
    try:
        await bot.send_message(
            chat_id=buyer_id,
            text="✅ **Оплата успешно подтверждена!**\n\n"
                 "Твой доступ к AI MEGA PACK v1.0 открыт. Держи ссылку на скачивание всех 5 файлов с Google Диска:\n"
                 f"👉 {GOOGLE_DRIVE_LINK}\n\n"
                 "Спасибо за покупку! Удачи в автоматизации рутины! 🚀"
        )
        await callback.message.edit_caption(caption=callback.message.caption + "\n\n🟢 ВЫДАНО")
    except Exception as e:
        await callback.message.answer(
            f"Ошибка отправки сообщения пользователю: {e}. Возможно, он заблокировал бота."
        )
    await callback.answer()

# Админ нажал "Отклонить"
@dp.callback_query(F.data.startswith("decline_"))
async def decline_payment(callback):
    buyer_id = int(callback.data.split("_")[1])
    
    try:
        await bot.send_message(
            chat_id=buyer_id,
            text="❌ **Оплата не найдена или чек некорректен.**\n\n"
                 "Если произошла ошибка, пожалуйста, свяжитесь с поддержкой напрямую."
        )
        await callback.message.edit_caption(caption=callback.message.caption + "\n\n🔴 ОТКЛОНЕНО")
    except Exception as e:
        pass
    await callback.answer()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())