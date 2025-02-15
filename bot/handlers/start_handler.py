from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram import types

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message:types.Message):
    await message.answer("Привет! Я бот для подготовки к госам\n Пиши вопросы_ пришлю ответы!)\n")