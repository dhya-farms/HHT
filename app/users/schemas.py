from typing import Optional, List

from pydantic.v1 import BaseModel, validator

from app.users.enums import UserType
from datetime import datetime

from app.utils.helpers import trim_mobile_no, allow_string_rep_of_enum


# User Creation Schema
class UserCreateSchema(BaseModel):
    name: str
    email: str
    mobile_no: str
    user_type: UserType

    # validator to trim  display number
    _validate_mobile_no = validator('mobile_no',
                                    allow_reuse=True,
                                    pre=True)(trim_mobile_no)

    # Validator to allow string version of enum value too
    _validate_user_type = validator('user_type',
                                    allow_reuse=True,
                                    pre=True)(allow_string_rep_of_enum)


# User Update Schema
class UserUpdateSchema(BaseModel):
    name: str
    email: str
    mobile_no: str
    user_type: UserType

    # validator to trim  display number
    _validate_mobile_no = validator('mobile_no',
                                    allow_reuse=True,
                                    pre=True)(trim_mobile_no)

    # Validator to allow string version of enum value too
    _validate_user_type = validator('user_type',
                                    allow_reuse=True,
                                    pre=True)(allow_string_rep_of_enum)


# User Listing Schema
class UserListSchema(BaseModel):
    name: Optional[str]
    email: Optional[str]
    mobile_no: Optional[str]
    user_type: Optional[UserType]
    # validator to trim  display number
    _validate_mobile_no = validator('mobile_no',
                                    allow_reuse=True,
                                    pre=True)(trim_mobile_no)

    # Validator to allow string version of enum value too
    _validate_user_type = validator('user_type',
                                    allow_reuse=True,
                                    pre=True)(allow_string_rep_of_enum)
