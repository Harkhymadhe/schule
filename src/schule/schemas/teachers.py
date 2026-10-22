# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, Field

__all__ = [
    "BaseTeacher",
    "PrimaryTeacher",
    "SecondaryTeacher",
    "CreatePrimaryTeacher",
    "CreateSecondaryTeacher",
    "DisplayPrimaryTeacher",
    "DisplaySecondaryTeacher",
]


class BaseTeacher(BaseModel):
    first_name: str = Field(..., description="Teacher's first name.")
    last_name: str = Field(..., description="Teacher's last name.")


class PrimaryTeacher(BaseTeacher):
    id: int = Field(..., description="Teacher ID.")
    grade: int = Field(..., gt=0, lt=6, description="Teacher's class")


class SecondaryTeacher(BaseTeacher):
    id: int = Field(..., description="Teacher ID.")
    subject_id: int = Field(..., description="Teacher subject ID.")


class CreatePrimaryTeacher(BaseTeacher):
    grade: int = Field(..., gt=0, lt=6, description="Teacher's class")


class UpdatePrimaryTeacher(BaseModel):
    first_name: Optional[str] = Field(default=None, description="Teacher's first name.")
    last_name: Optional[str] = Field(default=None, description="Teacher's last name.")
    grade: Optional[int] = Field(
        default=None, gt=0, lt=6, description="Teacher's class"
    )


class UpdateSecondaryTeacher(BaseModel):
    first_name: Optional[str] = Field(default=None, description="Teacher's first name.")
    last_name: Optional[str] = Field(default=None, description="Teacher's last name.")
    subject_id: Optional[int] = Field(default=None, description="Teacher subject ID.")


class CreateSecondaryTeacher(BaseTeacher):
    subject_id: int = Field(..., description="Teacher subject ID.")


class DisplayPrimaryTeacher(BaseTeacher):
    grade: int = Field(..., gt=0, lt=6, description="Teacher's class")


class DisplaySecondaryTeacher(BaseTeacher):
    subject_id: int = Field(..., description="Teacher subject ID.")
