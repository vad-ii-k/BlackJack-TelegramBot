from hashlib import sha256
from typing import Optional

from sqlalchemy import select
from sqlalchemy.engine import ChunkedIteratorResult

from app.admin.dataclasses import Admin
from app.admin.models import AdminModel
from app.base.base_accessor import BaseAccessor
from app.store.database.sqlalchemy_base import mapper_registry


class AdminAccessor(BaseAccessor):
    async def get_by_email(self, email: str) -> Optional[Admin]:
        async with self.app.database.session.begin() as session:
            query = select(Admin).where(Admin.email == email)
            result: ChunkedIteratorResult = await session.execute(query)
            admin: Admin = result.scalars().first()
            if admin:
                return admin

    async def create_admin(self, email: str, password: str) -> Admin:
        async with self.app.database.session.begin() as session:
            admin = Admin(
                email=email, password=sha256(password.encode()).hexdigest()
            )
            session.add(admin)
        return admin


mapper_registry.map_imperatively(Admin, AdminModel)
