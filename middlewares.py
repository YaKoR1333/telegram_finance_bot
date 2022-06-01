"""Пропускаем сообщения только от одного ТГ аккаунта"""
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AccessMiddleware(BaseMiddleware):
    def __init__(self, access_id: int):
        self.access_id = access_id
        super().__init__()

    async def on_progress_message(self, message: types.Message, _):
        if int(message.from_user.id) != int(self.access_id):
            await message.answer('Access Denied')
            raise CancelHandler()
