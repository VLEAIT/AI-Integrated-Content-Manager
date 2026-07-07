from fastapi import APIRouter,Depends,HTTPException,status
from schemas import WorkResponse,WorkBaseCreate,Role_type
from database import get_db
from typing import Annotated
from core import get_current_user
from sqlalchemy.orm import Session
from models import User,Workspace,Workspacealloc



router=APIRouter(
    prefix="/workspace",
    tags=["workspace"]
)

DatabaseSession=Annotated[Session,Depends(get_db)]
Current_User=Annotated[User,Depends(get_current_user)]

@router.post("/create",response_model=WorkResponse)
def create(workbase:WorkBaseCreate,db:DatabaseSession,current_user:Current_User):
    if current_user.role_type != Role_type.owner:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user profile doesnot match owner category")
    
    existing=db.query(Workspace).filter(Workspace.brand_name==workbase.brand_name,Workspace.owner_id==current_user.id).first() 
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="verification error")
    
    db_workspace=Workspace(**workbase.model_dump(),owner_id=current_user.id) 
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    
    db_alloc=Workspacealloc(
        user_id=current_user.id,
        workspace_id=db_workspace.id,
        allocated_role=current_user.role_type
    )

    db.add(db_alloc)
    db.commit()
    db.refresh(db_alloc)

    return db_workspace
    