from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('Главное меню')

"""Главное меню"""
btnStatistics = KeyboardButton('Статистика')
btnLastExpenses = KeyboardButton('Последние расходы')
btnCategories = KeyboardButton('Категории трат')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnLastExpenses).add(btnStatistics).insert(btnCategories)

"""Меню статистики"""
btnStatisticsDay = ('Cтатистика за день')
btnStatisticsWeek = ('Статистика за неделю')
btnStatisticsMonth = ('Cтатистика за месяц')
btnStatisticsYear = ('Статистика за год')
statisticsMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStatisticsDay).insert(btnStatisticsWeek)\
                                                          .add(btnStatisticsMonth).insert(btnStatisticsYear)\
                                                          .add(btnMain)
