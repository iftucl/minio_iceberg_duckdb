from fastapi import HTTPException
from typing import Optional, Union
from datetime import datetime
from pydantic import (
    BaseModel, 
    Field,
    EmailStr, 
    field_validator,
    ConfigDict,
)

from modules.utils.api_logger import local_logger

from modules.utils.ashing_utils import password_hashing

class MongoTraderUser(BaseModel):
    username: str = Field(examples=['my_username'],
                          description='username for API',
                          frozen=True, # makes immutable
                          )
    password: str = Field(description='my password', # used to be SecretStr
                                frozen=False, # makes mutable
                                exclude=False, # excludes pwd from serialization and printing
                          )
    email: EmailStr = Field(example='my_email@mydomain.com',
                            description='email address for the user',
                            frozen=True, # makes immutable
                            )

class TraderAuthRequest(MongoTraderUser):
    @field_validator('password', mode='before')
    @classmethod
    def set_password(cls, v: str) -> str:        
        return password_hashing(v)

class TraderAuthToken(MongoTraderUser):    
    token_expiry: Optional[Union[datetime, str]] = Field(description="JWT Token expiry time")

    @field_validator('token_expiry', mode='before')
    @classmethod
    def set_password(cls, v: str) -> str:
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError as ver:
                local_logger.error(f"Could not convert JWT Token Expiry to datetime from str: {ver}")
                raise
        if isinstance(v, datetime):
            return v
        return None


class CreateUserRequest(MongoTraderUser):
    model_config = ConfigDict(
        title="CreateUserRequest",
        json_schema_extra = {
            "description": "Create username and password"
            
        })

    @field_validator('password', mode='before')
    @classmethod
    def set_password(cls, v: str) -> str:        
        return password_hashing(v)

    @field_validator('username')
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if ' ' in v:
            raise ValueError('must NOT contain a space')
        return v

