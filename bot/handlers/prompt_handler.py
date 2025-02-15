from aiogram import Router
from aiogram.types import Message

prompt_router = Router()

@prompt_router.message()
async def msg_prompt(message:Message):
    await message.answer("Пока я ничего не умею, но вот что ты написал \n"+message.text)