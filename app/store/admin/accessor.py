import typing

from sqlalchemy import select

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def get_by_email(self, email: str) -> Admin | None:
        async with self.app.database.session() as session:
            admin = (await session.execute(
                select(AdminModel)
                .where(AdminModel.email == email)
            )).scalar()

        if not admin:
            return

        return admin.to_dc()

    async def create_admin(self, email: str, password: str) -> Admin:
        async with self.app.database.session.begin() as session:
            new_admin = AdminModel(email=email, password=password)
            session.add(new_admin)
            return new_admin.to_dc()
