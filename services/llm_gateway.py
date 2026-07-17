from core import settings
import os
from anthropic import Anthropic,APITimeoutError,APIStatusError
from datetime import time

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
        current_time=time.time()
        if current_time < self.circuit_open_until:
            remaining_seconds=int(self.circuit_open_until-current_time)
            print(f"Circuit is open .blocking calls for {remaining_seconds}")
            return " ai is generating"
        if  self.provider == "claude":
            return self._call_claude_with_retry(raw_description)
        
        def _call_claude_with_retry(self,prompt:str)->str:
            system_instruction=(
                "You are an expert social media copywriter and growth marketer."
                " Your task is to generate high-converting, platform-optimized captions for marketing posts and short-form video reels based on the user's provided context, images, or raw transcripts."
                "Output only the final caption without quotas")
            max_retries=3
            base_delay=1.0
            for attempt in range(max_retries):  
                try:
                    response=self.client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_token=1000,
                        temperature=0.7,
                        system=system_instruction,
                        message=[{"role":"user","content":f"Create a master caption for this:\n{prompt}"}]
                    )  
                    self.failure_count=0
                    self.circuit_open_until=0.0
                    return response.content[0].text.strip()
                except APITimeoutError:
                    print(f"claude took more than 8s on attempt{attempt + 1}/{max_retries}")
                except APIStatusError as e:
                    print(f"Upstream returned status code {e.status_code} on {attempt + 1}")
                except Exception as e:
                    print(f"Unexpected processing glitch in attempt {attempt + 1}:{e}")
                if attempt < max_retries - 1:
                    delay=base_delay * (2**attempt)
                    print(f"Retrying network connectivity link in {delay} seconds")
                    time.sleep(delay)
            self.failure_count += 1
            print(f"Consecutive failure registered :{self.failure_count}/{self.max_failures}")

            if self.failure_count >= self.max_failures:
                self.circuit_open_until=time.time() + self.countdown_period
                print(f"Critical: Circuit tripped open! shutting down system api call for{self.cooldown_period}") 
            return "The content creation system is temporarily delayed due to upstream server loads"                

                
            
            
ai_gateway=LLMGateway()           

