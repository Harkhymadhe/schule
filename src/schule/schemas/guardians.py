# -*- coding: utf-8 -*-

from typing import List
from pydantic import BaseModel, Field

__all__ = ["Guardian", "DisplayGuardian"]


class Guardian(BaseModel):
    id: str = Field(..., description="Guardian ID.")
    email: str = Field(..., description="Guardian email.")
    password: str = Field(..., description="Guardian password.")
    first_name: str = Field(..., description="Guardian's first name.")
    last_name: str = Field(..., description="Guardian's last name.")
    ward_ids: List[str] = Field(..., description="List of children IDs.")


class DisplayGuardian(BaseModel):
    id: str = Field(..., description="Guardian ID.")
    email: str = Field(..., description="Guardian email.")
    first_name: str = Field(..., description="Guardian's first name.")
    last_name: str = Field(..., description="Guardian's last name.")
    ward_ids: List[str] = Field(..., description="List of children IDs.")
