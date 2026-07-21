from sqlalchemy.orm import Session
from  models import PostMasterModel,AIstatus
from llm_gateway import ai_gateway
from database import get_db
from typing import Annotated
from fastapi import Depends

databasesession=Annotated[Session,Depends(get_db)]


def process_master_post_caption(masterpost_id:int,db:databasesession):
    post=db.query(PostMasterModel).filter(PostMasterModel.id==masterpost_id).first()
    if not post:
        return
    post.caption_ai_status=AIstatus.PROCESSING
    db.commit()

    try:
        generated_caption=ai_gateway.generate_social_caption(post.raw_description)

        if generated_caption.startswith("["):
            raise Exception(f"AI generated issue:{generated_caption}")
        
        post.ai_caption=generated_caption
        post.caption_ai_status=AIstatus.COMPLETED

    except Exception as e:
        post.caption_ai_status=AIstatus.FAILED
        post.caption_ai_error=str(e)
    finally:
        db.commit()        
