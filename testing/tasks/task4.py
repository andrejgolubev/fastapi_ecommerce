from fastapi import Depends , APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from database import get_async_db#type:ignore
from app.models.task import TaskModel #type:ignore   
from app.models.project import ProjectModel#type:ignore
from app.schemas.task import TaskUpdate, TaskSchema  #type:ignore

router = APIRouter() 


@router.put('/{task_id}', response_model=TaskSchema)
async def update_task(task: TaskUpdate, task_id: int, db: AsyncSession = Depends(get_async_db), ): 
    if task.project_id:
        stmt = (TaskModel.id == task_id, 
                TaskModel.is_active == True, 
                ProjectModel.id == task.project_id,
                ProjectModel.is_active == True)
        task_sc = await db.scalars(select(TaskModel).where(*stmt))
        task_fst = task_sc.first()
        if not task_fst: 
            raise HTTPException(status_code=404)

    await db.execute(update(TaskModel).where(*stmt).values(**task.model_dump()))
    await db.commit() 

    return task_fst
