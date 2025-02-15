from aiogram import types, Dispatcher
from aiogram import Bot as AiogramBotr

from .handlers import bootstrap

class Bot:
        
        def __init__(self, token:str):
            self.bot:AiogramBotr = AiogramBotr(token=token)
            self.dispatcher:Dispatcher = Dispatcher()
            
        
        async def start(self) -> None:
              self._set_up_routes()
              await self.dispatcher.start_polling(self.bot, polling_timeout=100)
        
        def _set_up_routes(self) -> None:
            self.dispatcher.include_router(bootstrap.start_router)

        