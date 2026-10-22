# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException

from schule.utils import authenticate_user_id
from schule.schemas.auth import User

__all__ = ["login"]


router = APIRouter(tags=["Authentication 🔒"], prefix="/login")


@router.post("/", status_code=200)
def login(user: User):
    try:
        response = authenticate_user_id(
            email=user.email,
            password=user.password,
            is_guardian=user.is_guardian,
        )
        return response
    except:
        raise HTTPException(
            status_code=404, detail=f"Unable to verify user: {user.email}."
        )
