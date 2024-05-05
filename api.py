from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, select, create_engine, SQLModel
from typing import List, Optional

# Define your SQLModel
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: str
    url: str
    image: str
    detail: str

# Define your FastAPI app
app = FastAPI()

# Database URL
DATABASE_URL = "sqlite:///data.db"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API endpoints
@app.get("/products/", response_model=List[Product])
def get_products(skip: int = 0, limit: int = 10):
    with Session(engine) as session:
        products = session.exec(select(Product).offset(skip).limit(limit)).all()
    return products

@app.get("/product/{product_id}", response_model=Product)
def get_product(product_id: int):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/search/", response_model=List[Product])
def search_products(query: str):
    with Session(engine) as session:
        # Perform a case-insensitive search for products containing the query string in their name or detail
        products = session.exec(select(Product).where(Product.name.ilike(f"%{query}%"))).all()
    return products

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
