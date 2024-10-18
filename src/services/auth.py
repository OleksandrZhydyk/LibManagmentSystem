from config import conf
from database.models import User
from dto.repository import SearchFieldDTO
from dto.service import TokenDTO
from repositories.user import UserRepository
from schemas.auth import UserLogin
from schemas.user import UserCreate
from security import sign_jwt, verify_password


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def register(self, user_create: UserCreate) -> TokenDTO:
        fields = [SearchFieldDTO(column="email", value=user_create.email)]
        if await self.user_repo.exists(search_fields=fields):
            raise ValueError(f"User email {user_create.email} already exists.")

        user_dct = user_create.model_dump(exclude={"confirmed_password"})

        user = await self.user_repo.create(**user_dct)
        return self._get_tokens(user)

    async def login(self, user_creds: UserLogin) -> TokenDTO:
        user = await self.authenticate_user(user_creds.email, user_creds.password)
        if not user:
            raise ValueError("Incorrect email or password.")
        return self._get_tokens(user)

    async def get_user(self, email: str) -> User:
        field = SearchFieldDTO(column="email", value=email)
        return await self.user_repo.get_one([field])

    async def authenticate_user(self, email: str, password: str) -> bool | User:
        user = await self.get_user(email)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user

    def _get_tokens(self, user: User) -> TokenDTO:
        access_token = sign_jwt({"email": user.email}, expiration_time=conf.ACCESS_TOKEN_LIFETIME)
        refresh_token = sign_jwt({"email": user.email}, expiration_time=conf.REFRESH_TOKEN_LIFETIME)
        return TokenDTO(access=access_token, refresh=refresh_token)
