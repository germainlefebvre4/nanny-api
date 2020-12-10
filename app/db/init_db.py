from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
# from app.db import base
from app.schemas.day_type import DayTypeCreate

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email=settings.USER_ADMIN_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.USER_ADMIN_EMAIL,
            firstname=settings.USER_ADMIN_FIRSTNAME,
            password=settings.USER_ADMIN_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)

    user = crud.user.get_by_email(db, email=settings.USER_TEST_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.USER_TEST_EMAIL,
            firstname=settings.USER_TEST_FIRSTNAME,
            password=settings.USER_TEST_PASSWORD,
            is_superuser=False,
        )
        user = crud.user.create(db, obj_in=user_in)
    
    for day_type_name in ["Présence enfant", "Maladie enfant"]:
        day_type_in = DayTypeCreate(name=day_type_name)
        crud.day_type.create(db=db, obj_in=day_type_in)
