import uuid
import asyncio
from services.social.base import BaseSocialPublisher

class StubPublisher(BaseSocialPublisher):
    async def publish(self, access_token:str, caption:str, media_url:str = None, **kwargs):
        await asyncio.sleep(1)
        return {"platform_post_id":f"mock_post_{uuid.uuid4().hex[:8]}","status":"PUBLISHED"}