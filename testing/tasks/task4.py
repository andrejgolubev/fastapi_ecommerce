from fastapi import Depends , APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_async_db
from app.models.task import TaskModel    
from app.models.project import ProjectModel
from app.schemas.task import TaskUpdate, TaskSchema  

router = APIRouter() 


@router.put('/{task_id}', response_model=TaskSchema)
async def create_task(task: TaskUpdate, task_id: int, db: AsyncSession = Depends(get_async_db), ): 
    if task.project_id:
        task = await db.scalars(select(TaskModel).where(TaskModel.id == task_id, 
                                                        TaskModel.is_active == True, 
                                                        TaskModel.project_id == task.project_id))
        if not task.first(): 
            raise HTTPException(status_code=404)
    
    task_model = TaskModel(**task.model_dump())
    db.add(task_model)
    await db.commit()

    return task_model