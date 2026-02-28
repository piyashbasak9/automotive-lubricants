from sqlalchemy.orm import Session
from models import User, Product
import schemas
from auth import get_password_hash

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name or user.username
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_products(db: Session):
    return db.query(Product).all()

def get_unique_categories(db: Session):
    categories = db.query(Product.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = Product(
        name=product.name,
        category=product.category,
        price=product.price,
        image=product.image
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
