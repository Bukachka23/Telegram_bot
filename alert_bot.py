from aiogram.dispatcher.filters import Text
import logging
import string
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext

API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Calling the keyboard
def get_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Оберiть мiсто'),KeyboardButton('Види загроз'))

    return kb

# Class for processing the state machine
class ClientStatesGroup(StatesGroup):

    city = State()
    desc = State()

# Decorator and asynchronous function that handles the /start command
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer('Вітаю у боті повітряної тривоги',
                         reply_markup=get_keyboard())

# Asynchronous function that handles inline buttons and calls the state of the "Select City" button
@dp.message_handler(Text(equals='Оберiть мiсто', ignore_case=True), state=None)
async def start_work(message: types.Message) -> None:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton('Харкiв(обл)', callback_data="#Харкiвська_область"),
        InlineKeyboardButton('Полтава(обл)', callback_data="#Полтавська_область"),
        InlineKeyboardButton('Суми(обл)', callback_data="#Сумська_область"),
        InlineKeyboardButton('Чернiгiв(обл)', callback_data="#Чернігівська_область"),
        InlineKeyboardButton('Дніпропетровськ(обл)', callback_data="#Дніпропетровська_область"),
        InlineKeyboardButton('Запоріжжя(обл)', callback_data="#Запорізька_область"),
        InlineKeyboardButton('Черкаси(обл)', callback_data="#Черкаська_область"),
        InlineKeyboardButton('Кропивницький(обл)', callback_data="#Кіровоградська_область"),
        InlineKeyboardButton('Донецьк(обл)', callback_data="#Донецька_область"),
        InlineKeyboardButton('Миколаїв(обл)', callback_data="#Миколаївська_область"),
        InlineKeyboardButton('Херсон(обл)', callback_data="#Херсонська_область"),
        InlineKeyboardButton('Київ(обл)', callback_data="#Київська_область"),
        InlineKeyboardButton('Вінниця(обл)', callback_data="#Вінницька_область"),
        InlineKeyboardButton('Житомир(обл)', callback_data="#Житомирська_область"),
        InlineKeyboardButton('Одеса(обл)', callback_data="#Одеська_область"),
        InlineKeyboardButton('Івано-Франківськ(обл)', callback_data="#ІваноФранківська_область"),
        InlineKeyboardButton('Луганськ(обл)', callback_data="#Луганська_область"),
        InlineKeyboardButton('Львів(обл)', callback_data="#Львівська_область"),
        InlineKeyboardButton('Рівне(обл)', callback_data="#Рівненська_область"),
        InlineKeyboardButton('Хмельницький(обл)', callback_data="#Хмельницька_область"),
        InlineKeyboardButton('Волинь(обл)', callback_data="#Волинська_область"),
        InlineKeyboardButton('Закарпаття', callback_data="#Закарпатська_область"),
        InlineKeyboardButton('Чернівеччина', callback_data="#Чернівецька_область")

    )
    await ClientStatesGroup.city.set()
    await message.reply("Оберіть, будь ласка, вашу область чи місто:", reply_markup=markup)

# A decorator that takes a lambda function as an argument to enumerate a list of values and handle callback query`() functions
@dp.callback_query_handler(lambda c: c.data in ["#Харкiвська_область",
                                                "#Полтавська_область",
                                                "#Сумська_область",
                                                "#Чернігівська_область",
                                                "#Дніпропетровська_область",
                                                "#Запорізька_область",
                                                "#Черкаська_область",
                                                "#Кіровоградська_область"
                                                "#Донецька_область",
                                                "#Миколаївська_область",
                                                "#Херсонська_область",
                                                "#Київська_область",
                                                "#Вінницька_область",
                                                "#Житомирська_область",
                                                "#Одеська_область",
                                                "#ІваноФранківська_область",
                                                "#Луганська_область",
                                                "#Львівська_область",
                                                "#Рівненська_область",
                                                "#Хмельницька_область",
                                                "#Волинська_область",
                                                "#Закарпатська_область",
                                                "#Чернівецька_область"])
# # Processing asynchronous functions and calling sfdifsl ygukn()
async def choose_word(callback_query: types.CallbackQuery):
    chosen_word = callback_query.data
    await bot.send_message(
        callback_query.from_user.id,
        "Ваша відповідь: {}".format(chosen_word)
    )
# Decorator and condition for checking incoming text
    @dp.message_handler()
    async def check_word(message: types.Message):
        if chosen_word in message.text.lower():
            await bot.send_message(
                message.from_user.id,
                "ТРЕВОГА! Є загроза ракетного обстрілу, приблизний час для укриття до 10 хвилин!"
            )

# Asynchronous function that handles inline buttons and calls the state of the "Types of threats" button
@dp.message_handler(Text(equals='Види загроз', ignore_case=True), state=None)
async def start_work(message: types.Message) -> None:
    await ClientStatesGroup.desc.set()
    await message.answer('Існує кілька типів сигналів:\nОдин довгий рівномірний гудок, який триває до 7 сек - попереджувальна сирена;\nГул, який наростає і знижується, триває одну хвилину і повторюється щонайменше тричі - загальна тривога (треба йти в укриття);\nДовгий і безперервний сигнал - повітряна тривога, ймовірно, ракета летить у ваш регіон.')

if __name__ == '__main__':
    executor.start_polling(dp)

