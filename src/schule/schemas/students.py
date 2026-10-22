# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, Field

__all__ = [
    "BaseStudent",
    "PrimaryStudent",
    "SecondaryStudent",
    "DisplayPrimaryStudent",
    "DisplaySecondaryStudent",
    "CreatePrimaryStudent",
    "CreateSecondaryStudent",
]


class BaseStudent(BaseModel):
    id: str = Field(..., description="Student ID.")
    guardian_id: str = Field(..., description="Guardian ID.")
    first_name: str = Field(..., description="Students's first name.")
    last_name: str = Field(..., description="Students's last name.")


class PrimaryStudent(BaseStudent):
    grade: int = Field(..., gt=0, lt=6, description="Student's class")


class SecondaryStudent(BaseStudent):
    email: str = Field(..., description="Student email.")
    password: str = Field(..., description="Student password.")
    grade: int = Field(..., gt=0, lt=7, description="Student's class")


class DisplayPrimaryStudent(BaseModel):
    id: str = Field(..., description="Student ID.")
    guardian_id: str = Field(..., description="Guardian ID.")
    first_name: str = Field(..., description="Students's first name.")
    last_name: str = Field(..., description="Students's last name.")
    grade: int = Field(..., description="Student's class")


class DisplaySecondaryStudent(DisplayPrimaryStudent):
    email: str = Field(..., description="Student email.")


class CreatePrimaryStudent(PrimaryStudent):
    id: Optional[str] = Field(default=None, description="Student ID.")
    guardian_id: Optional[str] = Field(default=None, description="Guardian ID.")
    guardian_first_name: str = Field(..., description="Guardian's first name.")
    guardian_last_name: str = Field(..., description="Guardian's last name.")


class CreateSecondaryStudent(SecondaryStudent):
    id: Optional[str] = Field(default=None, description="Student ID.")
    guardian_id: Optional[str] = Field(default=None, description="Guardian ID.")
    guardian_first_name: str = Field(..., description="Guardian's first name.")
    guardian_last_name: str = Field(..., description="Guardian's last name.")
    guardian_email: str = Field(..., description="Guardian email.")
    guardian_password: str = Field(..., description="Guardian password.")
