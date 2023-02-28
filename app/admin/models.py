from sqlalchemy import VARCHAR, Column, Integer

from app.store.database.sqlalchemy_base import db


class AdminModel(db):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(64), nullable=False, unique=True)
    password = Column(VARCHAR(64), nullable=False)
