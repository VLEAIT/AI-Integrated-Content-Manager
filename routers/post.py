from fastapi import APIRouter,Depends,status,BackgroundTasks,HTTPException
from models import PostChildModel,PostMasterModel
from schemas import PostChildResponse,PostChildCreate,MegaPostSubmission,statu,PostMasterResponse,PostApproval,PostChildUpdate
from typing import Annotated,List
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

def call_claude_api(prompt:str)->str:
    return f"Ai is generating idea"

def generate_ai_caption(masterpost_id:int):
    db=next(get_db)
    post=db.query(PostMasterModel).filter(PostMasterModel.id==masterpost_id).first()
    if post:
        ai_text=call_claude_api(prompt=post.raw_description)
        post.ai_caption=ai_text
        db.commit()
    

   
@router.post("/mega_submit",response_model=PostMasterResponse,status_code=status.HTTP_201_CREATED)
def mega_post_submission(Workspace_id:int,payload:MegaPostSubmission,db:DatabaseSession,memebership:access,current_user:CurrentUser,backgroundtask:BackgroundTasks):

    master_data=payload.master.model_dump()
    master_data["ai_caption"]="Processing via AI"
    db_masterpost=PostMasterModel(**master_data,workspace_id=Workspace_id,creator_id=current_user.id)
    db.add(db_masterpost)
    db.commit()
    db.refresh(db_masterpost)

    backgroundtask.add_task(generate_ai_caption,db_masterpost.id)


    for platform in payload.target_platform:
        db_child=PostChildModel(
            masterpost_id=db_masterpost.id, 
            platform =platform,
            approval_status=statu.pending,
            is_published=False,
            boost_budget=0.0
        )
        db.add(db_child)

    db.commit()  
    db.refresh(db_masterpost)      
    return db_masterpost


@router.get("/post_list",response_model=PostMasterResponse)
def list_workspace_posts(workspace_id:int,db:DatabaseSession,memebership:access,skip:int=0,limit:int=10):
    posts=db.query(PostMasterModel).filter(PostMasterModel.workspace_id==workspace_id).order_by(PostMasterModel.id.desc()).offset(skip).limit(limit).all()
    return posts


@router.patch("/child/{child_id}/approval", status_code=status.HTTP_200_OK)
def postapproval(workspace_id:int,child_id:int,payload:PostApproval,db:DatabaseSession,membership:access):
    child_post=db.query(PostChildModel).join(PostMasterModel).filter(PostChildModel.id==child_id,PostMasterModel.id==workspace_id).first()
    if not child_post:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Platform id idnot match ")
    child_post.approval_status=payload.approval_status
    db.commit()
    return {"message": f"Platform post updated to {payload.approval_status.value}"}



@router.put("/child/{child_id}/content",status_code=status.HTTP_200_OK)
def content_update(workspace_id:int,child_id:int,payload:PostChildUpdate,db:DatabaseSession,membership:access):
    child_content=db.query(PostChildModel).join(PostMasterModel).filter(PostChildModel.id==child_id,PostMasterModel.workspace_id==workspace_id).first()

    if not child_content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="data not found")
    
    child_content.boost_budget=payload.boost_budget
    child_content.scheduled_time=payload.scheduled_time
    db.commit()

    return {"message":"content child update succesfully"}




    

