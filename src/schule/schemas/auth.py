# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field

__all__ = ["User"]


class User(BaseModel):
    email: str = Field(..., description="User email.")
    password: str = Field(..., description="User password.")
    is_guardian: bool = Field(..., description="Whether or not user is a guardian.")
