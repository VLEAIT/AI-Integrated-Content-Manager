from abc import ABC,abstractmethod
from typing import Dict,Any,Optional

class BaseSocialPublisher(ABC):

    @abstractmethod
    async def publish(self,access_token:str,caption:str, media_url:str=None,**kwargs)->dict:
        pass