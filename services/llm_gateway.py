from core import settings
import os
from anthropic import Anthropic

class LLMGateway:

    def __init__(self):
        self.provider ="claude"

        try:
            self.client=Anthropic(api_key=settings.anthropic_api_key)
        except Exception as e:
            print(f"Gateway Intilization Error:{e}")
            self.client=None

    def generate_social_caption(self, raw_description:str)->str:
                



