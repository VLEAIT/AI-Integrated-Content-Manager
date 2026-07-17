from core import settings
import os
from anthropic import Anthropic

class LLMGateway:

    def __init__(self):
        self.provider ="claude"

        self.failure_count=0
        self.circuit_open_until=0.0
        self.max_failures=5
        self.cooldown_period=60
        

        try:
            self.client=Anthropic(api_key=settings.anthropic_api_key,timeout=8.0)
        except Exception as e:
            print(f"Gateway Intilization Error:{e}")
            self.client=None

    def generate_social_caption(self, raw_description:str)->str:
        if not self.client:
            return "Caption generation is offline (Missing api key)"
        if  self.provider == "claude":
            return self._call_claude(raw_description)
        
        def _call_claude(self,prompt:str)->str:
            system_instruction=(
                "You are an expert social media copywriter and growth marketer."
                " Your task is to generate high-converting, platform-optimized captions for marketing posts and short-form video reels based on the user's provided context, images, or raw transcripts."
                "Output only the final caption without quotas")
            try:
                response=self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_token=1000,
                    temperature=0.7,
                    system=system_instruction,
                    message=[
                        {"role":"user","content":f"Create a master caption for this:\n{prompt}"}
                    ]        
                )
                return response.content[0].text.strip()
            except Exception as e:
                print(f"LLM Provider Error:{str(e)}")
                return "Caption generation failed.please try again"
            
ai_gateway=LLMGateway()           

