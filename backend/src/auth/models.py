from pydantic import BaseModel


class Credentials(BaseModel):
    email: str
    password: str


class UserDetailsResponse(BaseModel):
    email: str
    is_admin: bool
    user_id: int
