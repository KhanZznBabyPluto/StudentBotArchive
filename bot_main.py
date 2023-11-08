from aiogram import types, executor, Bot, Dispatcher
from aiogram.types import CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import bot_keyboard as key
from bot_keyboard import get_kb, get_ikb, reactivate_kb, recieve_document_kb, times

from class_user import User, Group
from bot_mongo import *

user = User()
group = Group()

# users_col = connect_collection("users")
# book_col = connect_collection("book")

# users_col = students_db['Telegram id']
# group_id_col
# group_id = 


TOKEN_API = '6505220403:AAFqKWRmlSUqHlvMr7WTTVjZGLjj6GNFuOw'

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)
user = User()

class UserStates(StatesGroup):
    ACTIVE = State()
    INACTIVE = State() 

class ProfileStatesGroup(StatesGroup):
    name = State()
    surname = State()
    phone_number = State()
    university = State()
    faculty = State()
    group_number = State()



Action = """
    Давайте перейдём к учебным материалам и ссылкам\nЧтобы перейти к выбору предмета, нажмите <b>/Display_Subjects</b>\n"""

Action_for_start = """
    Дорбро пожаловать!\nЧтобы привязать ваш аккаунт, нажмите - <b>/Authorize</b>\nЧтобы перейти к выбору предмета, нажмите <b>/Display_Subjects</b>\n"""

Action_for_stop = """
    Бот остановлен. Вас нет в списках или вы неправильно ввели данные.\nПопробуйте ввести данные снова.\nЕсли это ошибка в списках, то обратитесь к авторам Бота - @Khangeldin_Ansar, @andrew0320"""


@dp.message_handler(commands=['Cancel'])
async def cmd_cancel(message: types.Message):
    await message.reply('Вы прервали сессию!\nБот приостановлен, для перезапуска нажмите кнопку ниже ↓', reply_markup= reactivate_kb)
    await UserStates.INACTIVE.set()


@dp.message_handler(commands=['Reactivate_bot'], state=UserStates.INACTIVE)
async def reactivate_bot(message: types.Message):
    await message.answer('Бот перезапущен')
    await message.answer(text= Action_for_start, parse_mode = 'HTML', reply_markup=get_kb())
    await UserStates.ACTIVE.set()


@dp.message_handler(commands=['Start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer(text = Action_for_start, parse_mode='HTML', reply_markup=get_kb())


@dp.message_handler(commands=['Authorize'])
async def cmd_create(message: types.Message) -> None:
    global user
    user = User()
    if check_key(["id"], [message.from_user.id]):
        await message.answer("Вы уже подключены, авторизовываться не надо")
        user.update_name(give_name_by_id(message.from_user.id), message.from_user.id)
        await message.answer(text = Action, parse_mode='HTML')
    else:
        await message.answer("Давайте привяжем вас к вашему аккаунту. Введите ваше имя")
        await ProfileStatesGroup.name.set() 


@dp.message_handler(lambda message: not message.text, state=ProfileStatesGroup.name)
async def check_name(message: types.Message):
    await message.reply('Это не имя!')

@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.name)
async def load_name(message: types.Message) -> None:
    global user
    if not check_key(["name"], [message.text]):
        await message.answer(text = Action_for_stop)
        await dp.bot.stop_poll(chat_id=message.from_user.id, message_id=message.message_id)
        await UserStates.INACTIVE.set()

    if message == 'admin':
        await message.answer('Введите пароль')
        await ProfileStatesGroup.password()
    else:
        user.update_name(message.text, message.from_user.id)
        await message.answer('Теперь отправьте свою фамилию')
        await ProfileStatesGroup.next()


@dp.message_handler(state = ProfileStatesGroup.password)
async def admin_keyboard(message: types.Message) -> None:
    if message == '12345':
        await message.answer('Для получения списка записей на сегодня, нажмите кнопку ниже ↓', reply_markup=recieve_document_kb)
    else:
        await message.asnwer('Пароль введён неверно!\nБот приостановлен')
        await dp.bot.stop_poll(chat_id=message.from_user.id, message_id=message.message_id)
        await UserStates.INACTIVE.set()

@dp.message_handler(commands = ['Receive_Document'])
async def document_push(message: types.Message):
    await message.answer('d;dwa') # здесь выгрузка документа


@dp.message_handler(lambda message: not message.text or message.text.isdigit(), state=ProfileStatesGroup.surname)
async def check_surname(message: types.Message):
    await message.reply('Это не фамилия!')

@dp.message_handler(state=ProfileStatesGroup.surname)
async def load_surname(message: types.Message) -> None:
    global user
    if not check_key(["name", "surname"], [user.name, message.text]):
        await message.answer(text = Action_for_stop)
        await dp.bot.stop_poll(chat_id=message.from_user.id, message_id=message.message_id)
        await UserStates.INACTIVE.set()

    user.update_surname(message.text)
    await message.answer('Введите Введите ваш номер телефона без различных пробелов и знаков')
    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) < 87000000000 or float(message.text) > 90000000000, state=ProfileStatesGroup.phone_number)
async def check_phone_number(message: types.Message):
    await message.reply('Введите реальный номер!')

@dp.message_handler(state=ProfileStatesGroup.phone_number)
async def load_phone_number(message: types.Message) -> None:
    global user
    user.update_phone(message.text)

    await message.answer('Введите название университета или выберите из списка')
    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: not message.text or message.text.isdigit(), state=ProfileStatesGroup.university)
async def check_univ(message: types.Message):
    await message.reply('Это не название!')

@dp.message_handler(state=ProfileStatesGroup.university)
async def load_university(message: types.Message) -> None:
    global user
    user.update_university(message.text)
    if not check_key(['name', 'surname', 'university'], [user.name, user.surname, user.univ]):
        await message.answer(text = Action_for_stop)
        await dp.bot.stop_poll(chat_id=message.from_user.id, message_id=message.message_id)
        await UserStates.INACTIVE.set()

    await message.answer('Введите название факультета или выберите из списка')
    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: not message.text or message.text.isdigit(), state=ProfileStatesGroup.faculty)
async def check_faculty(message: types.Message):
    await message.reply('Это не название!')

@dp.message_handler(state=ProfileStatesGroup.faculty)
async def load_faculty(message: types.Message) -> None:
    global user
    user.update_faculty(message.text)
    if not check_key(['name', 'surname', 'university', 'faculty'], [user.name, user.surname, user.univ, user.fac]):
        await message.answer(text = Action_for_stop)
        await dp.bot.stop_poll(chat_id=message.from_user.id, message_id=message.message_id)
        await UserStates.INACTIVE.set()

    await message.answer('Введите номер группы или выберите из списка')
    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 10000 or float(message.text) < 100, state=ProfileStatesGroup.group_number)
async def check_room_number(message: types.Message):
    await message.reply('Введите реальный номер!')

@dp.message_handler(state=ProfileStatesGroup.group_number)
async def load_room_number(message: types.Message,  state: FSMContext) -> None:
    global user
    user.update_group(message.text)
    if not check_key(['name', 'surname', 'university', 'faculty', 'group'], [user.name, user.surname, user.univ, user.fac, user.group]):
        await message.answer(text = Action_for_stop)
        await dp.bot.stop_poll(chat_id=message.from_user.id, message_id=message.message_id)
        await UserStates.INACTIVE.set()
    
    global group
    group.init_new(user.univ, user.fac)
    user.update_group_id(group.id)
    add_info(user.name, user.surname, user.phone, user.id, user.univ, user.fac, user.group, group.id)

    await message.answer(text = Action, parse_mode='HTML')
    await state.finish()



async def Add_Subject(message: types.Message, subject_name: str) -> None:
    # db = await MongoClient('localhost', 27017, 'my_database')

    subject = {'name': subject_name}
    # await db.subjects.insert_one(subject)

    await message.reply('Предмет "{}" добавлен успешно'.format(subject_name))



@dp.message_handler(commands=['add_subject'])
async def Add_Subject_Handler(message: types.Message) -> None:
    subject_name = await message.get_reply_message()
    await Add_Subject(message, subject_name)




async def Display_Subjects(message: types.Message) -> None:
    # subjects = await db.subjects.find_async()
    subjects = ['math', 'chemistry']

    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in subjects:
        reply_markup.add(types.KeyboardButton(text=subject['name']))

    await message.reply('Вот список предметов:', parse_mode='markdown', reply_markup=reply_markup)

    subject_name = await message.get_reply_message()

    await Download_Materials(message, subject_name)


async def Download_Materials(message: types.Message, subject_name: str) -> None:
    # materials = await db.materials.find_async({'subject': subject_name})
    materials = ['link', 'book']
    reply_markup = types.ReplyKeyboardRemove()
    await message.reply('Вот материалы по предмету "{}"'.format(subject_name), parse_mode='markdown', reply_markup=reply_markup)
    for material in materials:
        await message.reply(material['content'], parse_mode='markdown')


@dp.message_handler(commands=['Display_Subjects'])
async def Display_Subjects_Handler(message: types.Message) -> None:
    await Display_Subjects(message)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)