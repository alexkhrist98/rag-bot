import logging

from aiogram import Router
from aiogram.types import Message

from backend.prompt_processor import PromptProcessor

prompt_router = Router()

@prompt_router.message()
async def msg_prompt(message:Message):
    await message.answer("УШёл обрабатывать запрос, скоро вернусь с ответом)")
    try:
        prompt_processor:PromptProcessor = PromptProcessor()
        result = await prompt_processor.aprocess_prompt(message.text)
        await message.answer(result)
    except Exception as e:
        logging.error(e)
        await message.answer("Что-то пошло не так, пока не могу вернуть ответ()")
    
        