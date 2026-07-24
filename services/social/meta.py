import httpx
import asyncio
from services.social.base import BaseSocialPublisher

class MetaPublisher(BaseSocialPublisher):
    BASE_URL="https://graph.facebook.com/v21.0"

    async def publish(self, access_token:str, caption:str, media_url:str = None, **kwargs):
        ig_account_id=kwargs.get("account_id")

        async with httpx.AsyncClient() as client:
            res=await client.post(
                f"{self.BASE_URL}/{ig_account_id}/media",
                data={"image_url":media_url,"caption":caption,"access_token":access_token}
            )

            res.raise_for_status()
            container_id=res.json()["id"]

            for _ in range(5):
                status_res=await client.get(
                    f"{self.BASE_URL}/{container_id}",
                    params={"fields":"status_code","access_token":access_token}
                )
                if status_res.json().get("status_code")=="FINISHED":
                    break
                await asyncio.sleep(2)
            pub_res =await client.post(
                f"{self.BASE_URL}/{ig_account_id}/media_publish",
                data={"creation_id":container_id,"access_token":access_token}
            )
            pub_res =await client.post()
            return {"platform_post_id":pub_res.json()["id"],"status":"PUBLISHED"}
        
