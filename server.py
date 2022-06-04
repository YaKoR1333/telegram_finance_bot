"Сервер ТГ бота"
import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import exceptions
import expenses
from categories import Categories
from middlewares import AccessMiddleware
import keyboards

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

logging.basicConfig(level=logging.INFO)

ACCESS_ID = os.getenv('TELEGRAM_ACCESS_ID')

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


class Form(StatesGroup):
    new_budget = State()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение в бот и помощь по боту"""
    await message.answer(
        'Бот для учёта финансов\n\n'
        'Добавить расход, например: 500 продукты\n'
        'Статистика за день: /today\n'
        'Статистика за месяц: /month\n'
        'Последние внесённые расходы: /expenses\n'
        'Категории трат: /categories', reply_markup=keyboards.mainMenu)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """удаляет одну запись"""
    row_id = int(message.text[4:])
    expenses.delete_expenses(row_id)
    answer_message = 'Удалил'
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Отправляет список категории расходов"""
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " +\
        ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories]))
    await message.answer(answer_message)


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Статистика трат за день"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['week'])
async def week_statistics(message: types.Message):
    """Статистика трат за день"""
    answer_message = expenses.get_week_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """Статистика трат за месяц"""
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['change budget'])
async def change_budget_input(message: types.Message):
    await Form.new_budget.set()
    await message.reply('Введите свой новый бюджет')


@dp.message_handler(state=Form.new_budget)
async def change_budget_output(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['sum_budget'] = int(message.text)
        except ValueError:
            await message.answer(str(exceptions.NotCorrectMessage('Некорректное сообщние. Введите целое число')))
            return
    expenses.update_budget(data['sum_budget'])
    answer_message = f'Ваш новый бюджет {data["sum_budget"]}'
    await message.answer(answer_message)
    await state.finish()


@dp.message_handler(commands=['year'])
async def year_statistics(message: types.Message):
    """Статистика трат за год"""
    answer_message = expenses.get_year_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['balance'])
async def show_balance(message: types.Message):
    """Показывает текущий баланс"""
    answer_message = expenses.get_balance()
    await message.answer(answer_message)



@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о расходах"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer('Расходов нет')
        return
    last_expenses_rows = [
        f'{expense.amount} руб. на {expense.category_name} — нажми '
        f'/del{expense.id} для удаления'
        for expense in last_expenses]
    answer_message = 'Последние сохранённые траты:\n\n* ' + '\n\n* '.join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет новый расход"""
    if message.text == 'Главное меню':
        await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=keyboards.mainMenu)

    elif message.text == 'Статистика':
        await bot.send_message(message.from_user.id, 'Статистика', reply_markup=keyboards.statisticsMenu)

    elif message.text == 'Бюджет':
        await bot.send_message(message.from_user.id, 'Бюджет', reply_markup=keyboards.budgetMenu)

    elif message.text == 'Баланс':
        await show_balance(message)

    elif message.text == 'Изменить бюджет':
        await change_budget_input(message)

    elif message.text == 'Последние расходы':
        await list_expenses(message)

    elif message.text == 'Категории трат':
        await categories_list(message)

    elif message.text == 'Cтатистика за день':
        await today_statistics(message)

    elif message.text == 'Статистика за неделю':
        await week_statistics(message)

    elif message.text == 'Cтатистика за месяц':
        await month_statistics(message)

    elif message.text == 'Статистика за год':
        await year_statistics(message)
    else:
        try:
            expense = expenses.add_expense(message.text)
        except exceptions.NotCorrectMessage as e:
            await message.answer(str(e))
            return
        answer_message = (
            f'Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n'
            f'{expenses.get_today_statistics()}\n\n'
            f'{expenses.get_balance()}')
        await message.answer(answer_message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
