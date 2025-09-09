from fastapi import FastAPI 
from app.database import Base, engine
from app.routers import categories, products, users, reviews


app = FastAPI() 

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(reviews.router)


@app.get('/') 
async def root(): 
    return {"message": "Добро пожаловать в API интернет-магазина!"}

'''
ВМЕСТО ЭТОГО МЕТОДА У НАС ЕСТЬ АЛЕМБИК
Этот Метод проверяет, существуют ли таблицы, описанные в Base.metadata (например, categories и products) и
создаёт только те таблицы, которых ещё нет в базе данных.
Может безопасно вызывается многократно, так как игнорирует существующие таблицы. (Идемпотентный, если ничего не переопределять.)'''