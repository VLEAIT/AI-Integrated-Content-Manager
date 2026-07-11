from fastapi import APIRouter,Depends,status
from models import PostChildModel,PostMasterModel
from schemas import PostChildResponse,PostChildCreate,MegaPostSubmission,statu
from typing import Annotated
from core import get_current_user,workspace_access
from database import get_db
from sqlalchemy.orm import Session
from models import User,Workspacealloc


router=APIRouter(
    prefix="/workspace/{workspace_id}/post",
    tags=["post"]
)

DatabaseSession=Annotated[Session,Depends(get_db)]
CurrentUser=Annotated[User,Depends(get_current_user)]
access=Annotated[Workspacealloc,Depends(workspace_access)]

@router.post("/mega_submit",response_model=MegaPostSubmission,status_code=status.HTTP_201_CREATED)
def mega_post_submission(Workspace_id:int,payload:MegaPostSubmission,db:DatabaseSession,memebership:access,current_user:CurrentUser):
    db_masterpost=PostMasterModel(**payload.master.model_dump(),workspace_id=Workspace_id,creator_id=current_user.id)
    db.add(db_masterpost)
    db.commit()
    db.refresh(db_masterpost)


    for platform in payload.target_platform:
        db_child=PostChildModel(
            masterpost_id=db_masterpost.id, 
            platform =platform,
            approved_status=statu.pending,
            is_published=False,
            boost_budget=0.0
        )
        db.add(db_child)
        db.commit()
        db.refresh(db_child)
    
