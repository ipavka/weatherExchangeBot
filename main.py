from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, ALLOWED_USERS
from pars import sinop, sinop_tomor, tempSevas
from banks_pars import genbank, rnkb

# инициализируем бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def auth(func):
    """ Фильтр по telegram id
     будет работать для id которые есть в списке"""
    async def wrapper(messages):
        if not messages['from']['id'] in ALLOWED_USERS:
            return await messages.reply("Access denied", reply=False)
        return await func(messages)

    return wrapper


@dp.message_handler(commands=['start', 'help'])
@auth
async def send_welcome(message: types.Message):
    await message.answer(f'Вот что я умею\n'
                         f'/today - погода на сегодня\n'
                         f'/tomor - погода на завтра\n'
                         f'/now - темперптура, ветер, рассвет/закат, история\n'
                         f'/genbank - курс ГЕНБАНК\n'
                         f'/rnkb - курс РНКБ\n'
                         f'/help - список команд')


@dp.message_handler(commands=['today'])
@auth
async def weather_today(message: types.Message):
    await message.answer(sinop())


@dp.message_handler(commands=['tomor'])
@auth
async def weather_tomor(message: types.Message):
    await message.answer(sinop_tomor())


@dp.message_handler(commands=['now'])
@auth
async def now(message: types.Message):
    await message.answer(tempSevas())


@dp.message_handler(commands=['genbank'])
@auth
async def kurs_genbank(message: types.Message):
    await message.answer(f'Курс Валют ГЕНБАНК\n'
                         f'{genbank()}')


@dp.message_handler(commands=['rnkb'])
@auth
async def kurs_rnkb(message: types.Message):
    await message.answer(f'Курс Валют РНКБ\n'
                         f'{rnkb()}')


@dp.message_handler()
@auth
async def add_expense(message: types.Message):
    await message.answer(f'Я понимаю только команды\n\n\n'
                         f'/today - погода на сегодня\n\n'
                         f'/tomor - погода на завтра\n\n'
                         f'/now - темперптура, ветер, рассвет/закат, история\n\n'
                         f'/genbank - курс ГЕНБАНК\n\n'
                         f'/rnkb - курс РНКБ\n\n'
                         f'/help - список команд')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
