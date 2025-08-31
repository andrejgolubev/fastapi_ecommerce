from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.categories import Category as CategoryModel
from app.schemas import Category as CategorySchema, CategoryCreate
from app.db_depends import get_db

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(db: Session = Depends(get_db), return_active: str = Query(
    description='Возвращать только активные категории? (y/n)', default='y')):
    """
    Возвращает список всех активных категорий.
    """
    stmt = select(CategoryModel).where(CategoryModel.is_active == True) if return_active=='y' else select(CategoryModel)
    categories = db.scalars(stmt).all()
    return categories



@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED) #response_model позволяет функции возвращать pydantic модель
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Проверка: указан ли parent_id
    if category.parent_id: #ЕСЛИ РОДИТЕЛЬ ЕСТЬ ТО ЕГО НАХОДИМ 
        stmt = select(CategoryModel).where(CategoryModel.id == category.parent_id)
        parent = db.scalars(stmt).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")

    # Создание новой категории
    category_model = CategoryModel(**category.model_dump()) # в скобках преобразуем Pydantic-модель CategoryCreate в словарь Python, 
    #затем распаковываем его, и оборачиваем в CategoryModel. на выходе получаем SQLAlchemy модель
    db.add(category_model)
    db.commit()
    db.refresh(category_model)
    return category_model


@router.put("/{category_id}")
async def update_category(category_id: int):
    """
    Обновляет категорию по её ID.
    """
    return {"message": f"Категория с ID {category_id} обновлена (заглушка)"}


@router.delete("/{category_id}", status_code=status.HTTP_200_OK, description='Delete category by ID')
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    stmt = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active == True)
    category = db.scalars(stmt).first()
    if not category: 
        raise HTTPException(status_code=404, detail='Category not found')
    
    db.execute(update(CategoryModel).where(CategoryModel.id == category_id).values(is_active=False))
    db.commit() 

    return {'status': 'success', 'message': f"Category with ID {category_id} is no more active"}
