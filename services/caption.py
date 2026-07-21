from sqlalchemy.orm import Session,Sess
from  models import PostMasterModel,AIstatus
from llm_gateway import ai_gateway
from database import get_db,SessionLocal
from typing import Annotated
from fastapi import Depends



def process_master_post_caption(masterpost_id:int)->None:
    db=SessionLocal()
    post=None
    try:
        post=db.query(PostMasterModel).filter(PostMasterModel.id==masterpost_id).first()
        if not post:
            return
        post.caption_ai_status=AIstatus.PROCESSING
        db.commit()

        ai_text=ai_gateway.generate_social_caption(prompt=post.raw_description)
        post.ai_caption=ai_text
        post.caption_ai_status=AIstatus.COMPLETED
        post.caption_ai_error=None
        db.commit()

    except Exception as e:
        db.rollback()

        if post:
            post.caption_ai_status=AIstatus.FAILED
            post.caption_ai_error=str(e)
            db.commit()

    finally:
        db.close()        



 
