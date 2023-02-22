from src.core.settings import settings
from src.models.users import Users
from src.services.users import UsersService
from src.db.db import Session


def admin_exist():
    with Session.begin() as session:
        admin = (
            session.query(Users)
            .filter(Users.username == settings.db_root_name)
            .first()
        )
        if not admin:
            admin = Users(
                username=settings.db_root_name,
                password_hashed=UsersService.hash_password(settings.db_root_password),
                role='admin',
            )
            session.add(admin)
