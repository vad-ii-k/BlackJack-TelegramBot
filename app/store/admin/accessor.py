from hashlib import sha256

from sqlalchemy import select
from sqlalchemy.engine import ChunkedIteratorResult

from app.admin.dataclasses import Admin
from app.base.base_accessor import BaseAccessor


class AdminAccessor(BaseAccessor):
    async def get_by_email(self, email: str) -> Admin | None:
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


# mapper_registry.map_imperatively(Admin, AdminModel)  # TODO: пофиксить
