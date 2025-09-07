from fastapi import Depends , APIRouter, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_async_db
from app.models.message import MessageModel  
from app.schemas.message import MessageSchema   


router = APIRouter() 


@router.get('/{message_id}', response_model=MessageSchema)
async def get_projects(message_id: int, db: AsyncSession = Depends(get_async_db), ): 
    scalars = await db.scalars(select(MessageModel).where(MessageModel.is_active == True, MessageModel.id == message_id))
    project = scalars.first()
    if project: 
        return project 
    else: 
        raise HTTPException(status_code=404, detail='Не найдено сообщения.')