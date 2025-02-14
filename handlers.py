from aiogram import Bot, Router, types, F
from aiogram.enums import ParseMode  # Исправленный импорт
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import API_TOKEN, CHAT_ID, SITE_URL  # Импортируем SITE_URL
from keyboards import main_keyboard
from aiogram import types
import os

bot = Bot(token=API_TOKEN)
router = Router()

# Определяем состояния
class Form(StatesGroup):
    name = State()
    topic = State()
    question = State()

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)

    # Путь к фото
    photo_path = 'photo/prostor.png'

    # Получаем изображение (если требуется сжать или обработать)
    try:
        # Пример сжимаем изображения или просто передаем без изменений
        if os.path.getsize(photo_path) < 5 * 1024 * 1024:  # Проверяем размер файла (5 MB)
            photo = types.FSInputFile(photo_path)  # Используем FSInputFile для отправки файла
            await message.answer_photo(
                photo=photo,  # Отправляем фото
                caption="🎉 Добро пожаловать в компанию Простор СМС! 📱\n\n"
                        "Мы специализируемся на отправке SMS-рассылок, рассылок через WhatsApp, Telegram и таргетированных рассылок для бизнеса и частных клиентов. 🌐🚀\n\n"
                        "Как я могу к вам обращаться? 😊",
                reply_markup=types.ReplyKeyboardRemove()  # Убираем клавиатуру
            )
        else:
            await message.answer("Изображение слишком большое для отправки. Пожалуйста, попробуйте другое.")

    except FileNotFoundError:
        await message.answer("Изображение не найдено.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")

# Получаем имя
@router.message(Form.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.topic)
    await message.answer(
        f"Приятно познакомиться, {message.text}! 😊\n\n"
        "Мы с радостью поможем вам! Наша компания предоставляет услуги по рассылке SMS, WhatsApp, Telegram и таргетированных рассылок для различных целей. 📱📲💬\n\n"
        "Выберите услугу, по которой хотите получить консультацию. 👇",
        reply_markup=main_keyboard()
    )

# Обработка выбора темы
@router.callback_query(F.data.in_(["СМС-Рассылка", "WhatsApp-Рассылка", "Другой вопрос"]))
async def handle_topic_selection(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.question)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer(
        f"Отлично, вы выбрали «{callback_query.data}». 📚\n"
        "Теперь, напишите одним сообщением ваш вопрос. Также, если хотите, укажите количество сообщений для рассылки. 💬📊"
    )

# Получение вопроса
@router.message(Form.question)
async def get_question(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_name = user_data.get("name", "Неизвестный")
    user_id = message.from_user.id
    user_nickname = message.from_user.username or "Нет никнейма"
    question = message.text

    # Отправляем сообщение администратору
    await bot.send_message(
        CHAT_ID,
        f"📩 *Новый вопрос!*\n\n"
        f"👤 *Пользователь:* {user_name} (@{user_nickname})\n"
        f"🆔 *ID:* {user_id}\n"
        f"💬 *Вопрос:* {question}",
        parse_mode=ParseMode.MARKDOWN  # Используем корректный режим разметки
    )

    # Отправляем сообщение пользователю с возможной ссылкой на сайт
    if SITE_URL:
        await message.answer(
            f"Ваш вопрос был успешно отправлен! Мы свяжемся с вами в ближайшее время. "
            f"Для получения дополнительной информации посетите наш сайт: "
            f"[Prostor-SMS]({SITE_URL})",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message.answer("Ваш вопрос был успешно отправлен! Мы свяжемся с вами в ближайшее время.")

    await state.clear()  # Сбрасываем состояние

