from fastapi import Depends , APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_async_db #type:ignore
from app.models.ticket import TicketModel  #type:ignore 
from app.schemas.ticket import TicketCreate , TicketSchema #type:ignore
from app.models.user import UserModel#type:ignore

router = APIRouter() 


@router.post('/', status_code=201, response_model=TicketSchema)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_async_db), ): 
    user_id = await db.scalars(select(UserModel).where(UserModel.id == ticket.user_id, 
                                                             UserModel.is_active == True, 
    ))

    if not user_id.first(): 
        raise HTTPException(status_code=400)
    ticket_model = TicketModel(**ticket.model_dump())
    db.add(ticket_model) 

    await db.commit()
    await db.refresh(ticket_model)

    return ticket_model