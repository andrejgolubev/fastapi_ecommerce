from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.categories import Category as CategoryModel
from app.schemas import Category as CategorySchema, CategoryCreate
from app.db_depends import get_db

from sqlalchemy.ext.asyncio import AsyncSession 
from app.db_depends import get_async_db

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

@router.get("/", response_model=list[CategorySchema], status_code=201)
async def get_all_categories(db: AsyncSession = Depends(get_async_db), return_active: str = Query(
    description='Возвращать только активные категории? (y/n)', default='y')
    ):

    stmt = select(CategoryModel).where(CategoryModel.is_active == True) if return_active=='y' else select(CategoryModel)
    categories = await db.scalars(stmt)
    return categories.all()



@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED) #response_model позволяет функции возвращать pydantic модель
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_async_db)):
    # Проверка: указан ли parent_id
    if category.parent_id: #ЕСЛИ РОДИТЕЛЬ ЕСТЬ ТО ЕГО НАХОДИМ 
        stmt = select(CategoryModel).where(CategoryModel.id == category.parent_id)
        result = await db.scalars(stmt)
        parent = result.first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")

    # Создание новой категории
    category_model = CategoryModel(**category.model_dump()) # в скобках преобразуем Pydantic-модель CategoryCreate в словарь Python, 
    #затем распаковываем его, и оборачиваем в CategoryModel. на выходе получаем SQLAlchemy модель
    db.add(category_model)
    await db.commit()
    await db.refresh(category_model)


    return category_model


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(category_id: int, category: CategoryCreate, db: AsyncSession = Depends(get_async_db)):
    
    # Проверяем существование категории
    stmt = select(CategoryModel).where(CategoryModel.id == category_id)
    result = await db.scalars(stmt)
    db_category = result.first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Проверяем parent_id, если указан
    if category.parent_id:
        stmt = select(CategoryModel).where(CategoryModel.id == category.parent_id)
        result = await db.scalars(stmt)
        parent = result.first()
        if not parent:
            raise HTTPException(status_code=400, detail="Parent category not found")
        if parent.id == category_id:
            raise HTTPException(status_code=400, detail="Category cannot be its own parent")

    # Обновляем категорию
    update_data = category.model_dump(exclude_unset=True) 
    # exclude_unset=True -> фильтруем только явно установленные поля, игнорируя значения по умолчанию и не переданные поля.
    await db.execute(
        update(CategoryModel)
        .where(CategoryModel.id == category_id)
        .values(**update_data)
    )
    await db.commit()
    return db_category



@router.delete("/{category_id}", response_model=CategorySchema)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_async_db)):
    
    stmt = select(CategoryModel).where(CategoryModel.id == category_id)
    result = await db.scalars(stmt)
    db_category = result.first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    await db.execute(
        update(CategoryModel)
        .where(CategoryModel.id == category_id)
        .values(is_active=False)
    )
    await db.commit()
    return db_category



@router.delete("/", status_code=status.HTTP_200_OK, description='Delete multiple categories by ID')
async def delete_multiple_categories(category_ids: str = Query(description='Comma-separated IDs'), db: AsyncSession = Depends(get_async_db)):
    try:
        category_ids_list = [int(id.strip()) for id in category_ids.split(',')]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category IDs format")
    
    stmt = select(CategoryModel).where(CategoryModel.id.in_(category_ids_list), CategoryModel.is_active == True)
    result = await db.scalars(stmt)
    category_objects = result.all()

    if not category_objects: 
        raise HTTPException(status_code=404, detail='Categories not found')
    
    await db.execute(update(CategoryModel).where(CategoryModel.id.in_(category_ids_list)).values(is_active=False))
    await db.commit() 

    names_found = [cat.name for cat in category_objects]
    ids_found = [cat.id for cat in category_objects]
    
    if len(names_found)==1:
        message = f"Category {names_found} with ID {ids_found} is no more active" 
    else: 
        message = f"Categories {names_found} with IDs {ids_found} are no more active" 

    return {'status': 'success', 'message': message}


@router.patch("/", status_code=status.HTTP_200_OK, description='Restore multiple categories by ID')
async def restore_multiple_categories(category_ids: str = Query(description='Comma-separated IDs'), db: AsyncSession = Depends(get_async_db)):
    try:
        category_ids_list = [int(id.strip()) for id in category_ids.split(',')]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category IDs format")
    
    stmt = select(CategoryModel).where(CategoryModel.id.in_(category_ids_list), CategoryModel.is_active == False)
    result = await db.scalars(stmt)
    category_objects = result.all()

    if not category_objects: 
        raise HTTPException(status_code=404, detail='Categories not found')
    
    await db.execute(update(CategoryModel).where(CategoryModel.id.in_(category_ids_list)).values(is_active=True))
    await db.commit() 

    names_found = [cat.name for cat in category_objects]
    ids_found = [cat.id for cat in category_objects]
    
    if len(names_found)==1:
        message = f"Category {names_found} with ID {ids_found} is now active" 
    else: 
        message = f"Categories {names_found} with IDs {ids_found} are now active" 

    
    return {'status': 'success', 'message': message}