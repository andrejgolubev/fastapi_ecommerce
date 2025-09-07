from fastapi import Depends , APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_async_db
from app.models.ticket import TicketModel   
from app.schemas.ticket import TicketCreate , TicketSchema 
from app.models.user import UserModel

router = APIRouter() 


@router.post('/', status_code=201, response_model=TicketSchema)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_async_db), ): 
    if ticket.user_id: 
        user_id = await db.scalars(select(TicketModel).where(TicketModel.user_id == ticket.user_id, 
                                                             TicketModel.is_active == True))
        if not user_id.first(): 
            raise HTTPException(status_code=404)
    ticket_model = await TicketModel(**ticket.model_dump())
    db.add(ticket_model) 

    await db.commit()
    await db.refresh(ticket_model)

    return ticket_model