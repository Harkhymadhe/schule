# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, Field

__all__ = [
    "BaseSubject",
    "UpdateSubject",
    "PrimarySubject",
    "SecondarySubject",
    "CreatePrimarySubject",
    "CreateSecondarySubject",
    "UpdateSubject",
    "UpdatePrimarySubject",
    "UpdateSecondarySubject",
]


class BaseSubject(BaseModel):
    name: str = Field(..., description="Name of subject.")
    description: str = Field(..., description="Description of subject.")


class PrimarySubject(BaseSubject):
    id: Optional[int] = Field(default=None, description="Identifier for subject.")


class SecondarySubject(BaseSubject):
    id: Optional[int] = Field(default=None, description="Identifier for subject.")
    min_class_grade: int = Field(..., description="Minimum class grade for subject.")
    max_class_grade: int = Field(..., description="Maximum class grade for subject.")


class CreatePrimarySubject(BaseSubject):
    pass


class CreateSecondarySubject(BaseSubject):
    min_class_grade: int = Field(..., description="Minimum class grade for subject.")
    max_class_grade: int = Field(..., description="Maximum class grade for subject.")


class UpdateSubject(BaseSubject):
    name: Optional[str] = Field(default=None, description="Name of subject.")
    description: Optional[str] = Field(
        default=None, description="Description of subject."
    )


class UpdatePrimarySubject(UpdateSubject):
    pass


class UpdateSecondarySubject(UpdateSubject):
    min_class_grade: Optional[int] = Field(
        default=None, description="Minimum class grade for subject."
    )
    max_class_grade: Optional[int] = Field(
        default=None, description="Maximum class grade for subject."
    )
