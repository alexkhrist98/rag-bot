from gigachat import GigaChat

from .llms.functions import get_base64_credentials


class MonitoringProvider:
    
    def __init__(self):
        credentials = get_base64_credentials()
        self.chat:GigaChat = GigaChat(
            credentials=credentials,
            verify_ssl_certs=False
        )
    
    async def aprovide_balance(self) -> dict:
        balance = await self.chat.aget_balance()
        balance_result = {}
        
        for item in balance.dict()['balance']:
            if item['usage'] == 'GigaChat':
                balance_result['model'] = item['value']
            elif item['usage'] == 'embeddings':
                balance_result['embeddings'] = item['value']
            
        return balance_result
