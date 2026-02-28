from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
import auth
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Automotive Lubricants API")

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Startup: populate with initial data ----------
@app.on_event("startup")
def startup_populate():
    db = next(get_db())
    # Create a test user if not exists
    if not crud.get_user_by_username(db, "test1"):
        test_user = schemas.UserCreate(username="test1", password="test123", full_name="Test User1")
        crud.create_user(db, test_user)

    # Populate products if empty
    if not crud.get_all_products(db):
        mock_products = [
            {"name": "PIAA Premium Oil - Cars", "category": "Cars", "price": 25.99, "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHf7CGYHcfPscGMo9ubwwZBdK4UHIh5WdE7w&s.jpg"},
            {"name": "PIAA Synthetic Oil - Bikes", "category": "Bikes", "price": 15.50, "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQKXEVzLzp537gtmZFyrv8fFRmn7rsRsBTCqg&s.jpg"},
            {"name": "PIAA CNG Engine Oil", "category": "CNG", "price": 22.00, "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTz-auwiJT-lVXbIaitSNrjbg0DWG-YsN8fw&s.jpg"},
            {"name": "PIAA Heavy Duty Oil - Trucks", "category": "Truck & Buses", "price": 18.75, "image": "https://www.mobil.com/lubricants/-/media/project/wep/mobil/mobil-row-us-1/oil-filters-update/mobil-1-products/mobil-1-proudcts-1200-x-630.jpg"},
            {"name": "PIAA Full Synthetic - Cars", "category": "Cars", "price": 32.99, "image": "https://fuelcurve.com/wp-content/uploads/2020/12/COMP-Pour.jpg"},
            {"name": "PIAA Bike Lubricant", "category": "Bikes", "price": 12.50, "image": "https://dxm.content-center.totalenergies.com/api/wedia/dam/transform/xysh7dg731tahpu9phz6cbk89o/total-quartz-jpg.webp.jpg"},
            {"name": "PIAA Auto Lubricant", "category": "Auto", "price": 15.50, "image": "https://cdn.shopify.com/s/files/1/0773/5892/3969/files/VP_Racing__Powersports_Sub_Zero_2T_Snowmobile_Full_Synthetic_Oil_1gal.webp?v=1757356528.jpg"},
        ]
        for prod in mock_products:
            db.add(models.Product(**prod))
        db.commit()
    db.close()

# ---------- API Endpoints ----------
@app.post("/api/signup", response_model=schemas.TokenResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = crud.create_user(db, user)
    token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer", "username": user.username, "full_name": new_user.full_name}

@app.post("/api/login", response_model=schemas.TokenResponse)
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, user_data.username)
    if not user or not auth.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = auth.create_access_token(data={"sub": user_data.username})
    return {"access_token": token, "token_type": "bearer", "username": user_data.username, "full_name": user.full_name}

@app.get("/api/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)

@app.post("/api/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    return {"categories": crud.get_unique_categories(db)}

@app.get("/api/user/{username}")
def get_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username, "full_name": user.full_name}