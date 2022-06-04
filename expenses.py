"""удаление, добавление, статистика расходов"""
import datetime
import re
from typing import NamedTuple, List, Optional
import pytz
import db
import exceptions
from categories import Categories


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""
    amount: int
    category_text: str


class Expense(NamedTuple):
    """Структура добавленного  в БД нового расхода"""
    id: Optional[int]
    amount: int
    category_name: str


def add_expense(raw_message: str) -> Expense:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(parsed_message.category_text)
    inserted_row_id = db.insert_db("expense", {
        "amount": parsed_message.amount,
        "created": _get_now_formatted(),
        "category_codename": category.codename,
        "raw_text": raw_message
    })
    return Expense(id=None,
                   amount=parsed_message.amount,
                   category_name=category.name)


def get_today_statistics() -> str:
    """Возвращает строкой статистики расходов за день"""
    cursor = db.get_cursor()
    cursor.execute('SELECT SUM(amount) '
                   'FROM expense WHERE date(created) = date("now", "localtime")')
    result = cursor.fetchone()
    if not result[0]:
        return 'Сегодня вы не тратили деньги'
    all_today_expense = result[0]
    cursor.execute('SELECT category.name, SUM(expense.amount) '
                   'FROM expense LEFT JOIN category '
                   'ON category.codename = expense.category_codename '
                   'WHERE DATE(created) = date("now", "localtime")'
                   'GROUP BY 1 '
                   'ORDER BY amount DESC ')
    results = cursor.fetchall()
    expenses_results = [Expense(id=None, amount=result[1], category_name=result[0]) for result in results]
    expenses_results_rows = [
        f'{expense.amount} руб. на {expense.category_name}'
        for expense in expenses_results]
    return (f'Расходы сегодня:\n'
            f'всего - {all_today_expense} руб.\n\n'
            f'Из них потрачено:\n\n' + '\n'.join(expenses_results_rows))


def get_week_statistics() -> str:
    """Возвращает строкой статистики расходов за неделю"""
    now = _get_now_datetime()
    first_day_of_week = f'{now.year:04d}-{now.month:02d}-{(now.day - datetime.datetime.now().weekday()):02d}'
    result = _expenses_period(first_day_of_week)
    if not result[0]:
        return 'На этой неделе ещё не было расходов'
    all_week_expenses = result[0]
    expenses_results_rows = _expenses_category_period(first_day_of_week)
    return (f'Расходы за неделю:\n'
            f'всего - {all_week_expenses} руб.\n\n'
            f'Из них потрачено:\n\n' + '\n'.join(expenses_results_rows))


def get_month_statistics() -> str:
    """Возвращает строкой статистики расходов за месяц"""
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    result = _expenses_period(first_day_of_month)
    if not result[0]:
        return 'В этом месяце ещё не было расходов'
    all_month_expenses = result[0]
    expenses_results_rows = _expenses_category_period(first_day_of_month)
    return (f'Расходы за месяц:\n'
            f'всего - {all_month_expenses} руб.\n\n'
            f'Из них потрачено:\n\n' + '\n'.join(expenses_results_rows))


def get_year_statistics() -> str:
    """Возвращает строкой статистики расходов за год"""
    now = _get_now_datetime()
    first_day_of_year = f'{now.year:04d}-01-01'
    result = _expenses_period(first_day_of_year)
    if not result[0]:
        return 'В этом году ещё не было расходов'
    all_year_expenses = result[0]
    expenses_results_rows = _expenses_category_period(first_day_of_year)
    return (f'Расходы за год:\n'
            f'всего - {all_year_expenses} руб.\n\n'
            f'Из них потрачено:\n\n' + '\n'.join(expenses_results_rows))


def last() -> List[Expense]:
    """Возвращает последние расходы"""
    cursor = db.get_cursor()
    cursor.execute('SELECT expense.id, expense.amount, category.name '
                   'FROM expense LEFT JOIN category '
                   'ON category.codename = expense.category_codename '
                   'ORDER BY created DESC limit 10')
    rows = cursor.fetchall()
    last_expenses = [Expense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]
    return last_expenses


def delete_expenses(row_id: int) -> None:
    """Удаляет сообщение по его идентификатору"""
    db.delete('expense', row_id)


def update_budget(new_budget: int) -> None:
    """Обновляет бюджет на месяц"""
    db.update('budget', 'month_limit', new_budget)


def _parse_message(raw_message: str) -> Message:
    """Парсит текст входящего сообщения о новом расходе"""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage('Не могу понять сообщение. Напишите сообщение в формате, '
                                           'например: \n1200 продукты')
    amount = regexp_result.group(1).replace(' ', '')
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом временной зоны Мск."""
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tz)
    return now


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime('%Y-%m-%d %H:%M:%S')


def _get_budget_limit() -> int:
    """Возвращает бюджет на месяц"""
    return db.fetch_all('budget', ['month_limit'])[0]['month_limit']


def get_balance() -> str:
    budget_limit = _get_budget_limit()
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    result = _expenses_period(first_day_of_month)
    all_month_expenses = result[0]
    if not result[0]:
        return f'Ваш баланс {budget_limit} руб.'
    else:
        return f'Ваш баланс {budget_limit - all_month_expenses} руб.'


def _expenses_period(first_day_period: str) -> list:
    cursor = db.get_cursor()
    cursor.execute(f'SELECT SUM(amount) '
                   f'FROM expense WHERE DATE(created) >= "{first_day_period}"')
    result = cursor.fetchone()
    return result


def _expenses_category_period(first_day_period: str) -> list:
    cursor = db.get_cursor()
    cursor.execute(f'SELECT category.name, SUM(expense.amount) '
                   f'FROM expense LEFT JOIN category '
                   f'ON category.codename = expense.category_codename '
                   f'WHERE DATE(created) >= "{first_day_period}"'
                   f'GROUP BY 1 '
                   f'ORDER BY amount DESC')
    results = cursor.fetchall()
    expenses_results = [Expense(id=None, amount=result[1], category_name=result[0]) for result in results]
    expenses_results_rows = [
        f'{expense.amount} руб. на {expense.category_name}'
        for expense in expenses_results]
    return expenses_results_rows
