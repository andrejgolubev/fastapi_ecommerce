# from db import async_session
# from models import Product
# from sqlalchemy import select, func

# temp_avg = await async_session.scalars(select(Product).where(Product.price))
# prices = [product.price for product in temp_avg.all()]
# avg = sum(prices) / len(prices)

# temp = await async_session.scalars(select(Product).where(Product.price > avg))
# result = temp.all()