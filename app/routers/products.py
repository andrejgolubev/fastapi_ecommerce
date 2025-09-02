from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import select, update
from app.models.products import Product as ProductModel
from app.schemas import Product as ProductSchema, ProductCreate
from app.db_depends import get_db, get_async_db
from sqlalchemy.orm import Session
from .categories import CategoryModel
from sqlalchemy.ext.asyncio import AsyncSession 



# Создаём маршрутизатор для товаров
router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", response_model=ProductSchema, status_code=200)
async def get_all_products(db: AsyncSession = Depends(get_async_db)):
    stmt = select(ProductModel).where(ProductModel.is_active == True, CategoryModel.is_active == True)
    result = await db.scalars(stmt)
    db_products = result.all()
    if not db_products: 
        raise HTTPException(status_code=404, detail='Не найдено продуктов.')
    
    return result


@router.post("/", response_model=ProductSchema, status_code=200)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_async_db)):

    if not product.category_id: 
        raise HTTPException(status_code=404, detail="Category not found")
    

    product_model = ProductModel(**product.model_dump())
    db.add(product_model)
    await db.commit()

    return product_model


# ОБЯЗАТЕЛЬНО list[ProductSchema] тк продуктов а значит и json responses будет много 
@router.get("/category/{category_id}", response_model=list[ProductSchema], status_code=200)
async def get_products_by_category(category_id: int = Path(), db: AsyncSession = Depends(get_async_db)):

    category_result = await db.scalars(
        select(CategoryModel)
        .where(CategoryModel.id == category_id, CategoryModel.is_active == True))
    category = category_result.first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found or inactive")
    
    products = await db.scalars(select(ProductModel).where(ProductModel.category_id == category.id, ProductModel.is_active == True))
    return products.all()



@router.get("/{product_id}", status_code=200, response_model=ProductSchema)
async def get_product(product_id: int = Path(), choice: str = Query(description='show inactive products? (y/n)', default='n'), db: AsyncSession = Depends(get_async_db)):
    
    if choice.lower() == 'n':
        stmt = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
        additional_detail = ' or inactive' 
    else: 
        stmt = select(ProductModel).where(ProductModel.id == product_id)
        additional_detail = ''
    scalars = await db.scalars(stmt)
    db_product = scalars.first()   
    if not db_product: 
        raise HTTPException(detail="Product not found" + additional_detail, status_code=404)
    
    return db_product


@router.put("/{product_id}", status_code=200, response_model=ProductSchema)
async def update_product(product_input: ProductCreate, product_id: int = Path(), db: AsyncSession = Depends(get_async_db)):
    stmt = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    result = await db.scalars(stmt)
    db_product = result.first()
    if not db_product: 
        raise HTTPException(status_code=404, detail="Product not found") 
    
    category_result = await db.scalars(select(CategoryModel).where(CategoryModel.id == db_product.category_id, CategoryModel.is_active == True))
    category = category_result.first()

    if not category: 
        raise HTTPException(status_code=404,
                            detail="Category not found or inactive")
    
    await db.execute(update(ProductModel).where(ProductModel.id == product_id).values(**product_input.model_dump()))
    await db.commit()
    
    return db_product

@router.delete("/{product_id}")
async def delete_product(product_id: int = Path(), db: AsyncSession = Depends(get_async_db)):
    result = await db.scalars(select(ProductModel).where(
        ProductModel.id == product_id,
        ProductModel.is_active == True))
    
    product = result.first()
    
    if not product: 
        raise HTTPException(status_code=404, detail='Product not found or it`s already been marked as inactive')
    

    await db.execute(
        update(ProductModel).where(ProductModel.id == product_id).values(is_active = False)
    )
    await db.commit() 

    return {"message": f"Product {product.name} has been marked as inactive"}

@router.patch("/{product_id}")
async def restore_product(product_id: int = Path(), db: AsyncSession = Depends(get_async_db)):
    search = await db.scalars(select(ProductModel).where(ProductModel.id == product_id,
                                                    ProductModel.is_active == False))
    product = search.first()
    if not product:     
        raise HTTPException(status_code=404, detail= f'Product is already active and doesn`t need to be restored.')
    
    await db.execute(
        update(ProductModel).where(ProductModel.id == product_id).values(is_active = True)
    )
    await db.commit() 

    return {"message": f"Product {product.name} has been marked as active"}