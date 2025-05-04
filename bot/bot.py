import os
import asyncio
import logging

from aiogram import types, Dispatcher
from aiogram import Bot as AiogramBotr

from backend.monitoring_provider import MonitoringProvider
from .handlers import bootstrap

class Bot:
        ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')      
        def __init__(self, token:str):
            self.bot:AiogramBotr = AiogramBotr(token=token)
            self.monitor:MonitoringProvider = MonitoringProvider()
            self.dispatcher:Dispatcher = Dispatcher()
            
        
        async def start(self) -> None:
              self._set_up_routes()
              logging.info("Routes are ready. Starting bot!")
              self._set_up_monitoring()
              await self.dispatcher.start_polling(self.bot, polling_timeout=100)
        
        async def _report_balance(self) -> None:
            logging.info('Starting balance monitoring')
            while True:
                 try:
                    balance = await self.monitor.aprovide_balance()
                    if balance['model'] < 10_000:
                        await self.bot.send_message(self.ADMIN_USER_ID, f'Баланс токенов модели меньше 10 000')
                    if balance['embeddings'] < 10_000:
                        await self.bot.send_message(self.ADMIN_USER_ID, 'Баланс токенов embeddings меньше 10 000!')
                           
                 except Exception as e:
                      logging.error(f'Failed fething balance \n{e}')
                      await self.bot.send_message(self.ADMIN_USER_ID, f'Не удалось получить баланс токенов \n{e}')
                 await asyncio.sleep(60)
                

        def _set_up_monitoring(self) -> None:
            logging.info('Starting monitroing')
            loop = asyncio.get_event_loop()
            loop.create_task(self._report_balance())
            
        
        def _set_up_routes(self) -> None:
            self.dispatcher.include_router(bootstrap.start_router)
            self.dispatcher.include_router(bootstrap.prompt_router)

        