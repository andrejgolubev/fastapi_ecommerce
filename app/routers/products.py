from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import select, update
from app.models.products import Product as ProductModel
from app.schemas import Product as ProductSchema, ProductCreate
from app.db_depends import get_db
from sqlalchemy.orm import Session
from .categories import CategoryModel

# Создаём маршрутизатор для товаров
router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", response_model=list[ProductSchema], status_code=200)
async def get_all_products(db: Session = Depends(get_db)):
    stmt = select(ProductModel).where(ProductModel.is_active == True, CategoryModel.is_active == True)
    result = db.scalars(stmt).all()
    if not result: 
        raise HTTPException(status_code=404, detail='Не найдено продуктов.')
    
    return result

@router.post("/", response_model=ProductSchema, status_code=200)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    if not product.category_id: 
        raise HTTPException(status_code=404, detail="Category not found")
    
    product_model = ProductModel(**product.model_dump())
    db.add(product_model)
    db.commit()
    db.refresh(product_model)
    return product_model



@router.get("/category/{category_id}", response_model=ProductSchema, status_code=200)
async def get_products_by_category(category_id: int = Path(), db: Session = Depends(get_db)):
    stmt = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active == True)
    category = db.scalars(stmt).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    products = db.scalars(select(ProductModel.category_id == category_id, ProductModel.is_active == True)).all()
    return products 



@router.get("/{product_id}", status_code=200, response_model=ProductSchema)
async def get_product(product_id: int = Path(), db: Session = Depends(get_db)):
    stmt = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    result = db.scalars(stmt).first()   
    if not result: 
        raise HTTPException(detail="Product not found or inactive", status_code=404)
    return result


@router.put("/{product_id}", status_code=200, response_model=ProductSchema)
async def update_product(product_input: ProductCreate, product_id: int = Path(), db: Session = Depends(get_db)):
    stmt = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    db_product = db.scalars(stmt).first() 
    if not db_product: 
        raise HTTPException(status_code=404, detail="Product not found") 
    
    category = db.scalars(select(CategoryModel).where(CategoryModel.id == db_product.category_id, CategoryModel.is_active == True))
    if not category: 
        raise HTTPException(status_code=404,
                            detail="Category not found or inactive")


    db.execute(update(ProductModel).where(ProductModel.id == product_id).values(**product_input.model_dump()))
    db.commit()
    db.refresh(db_product)
    
    return db_product

@router.delete("/{product_id}")
async def delete_product(product_id: int = Path(), db: Session = Depends(get_db)):
    product = db.scalars(select(ProductModel).where(ProductModel.id == product_id,
                                                    ProductModel.is_active == True)).first()
    if not product: 
        raise HTTPException(status_code=404, detail='Product not found or it`s already been marked as inactive')
    


    db.execute(
        update(ProductModel).where(ProductModel.id == product_id).values(is_active = False)
    )
    db.commit() 

    return {"message": f"Product {product.name} has been marked as inactive"}

@router.patch("/{product_id}")
async def restore_product(product_id: int = Path(), db: Session = Depends(get_db)):
    product = db.scalars(select(ProductModel).where(ProductModel.id == product_id,
                                                    ProductModel.is_active == False)).first()
    if not product: 
        raise HTTPException(status_code=404, detail= f'Product is already active and doesn`t need to be restored.')
    
    db.execute(
        update(ProductModel).where(ProductModel.id == product_id).values(is_active = True)
    )
    db.commit() 

    return {"message": f"Product {product.name} has been marked as active"}