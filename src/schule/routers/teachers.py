# -*- coding:utf-8 -*-

from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException

from schule.utils import (
    push_teacher_to_db,
    pull_teachers_from_db,
    delete_teacher_from_db,
    update_teacher_in_db,
)
from schule.schemas import DisplayPrimaryTeacher, DisplaySecondaryTeacher, TeacherType
from schule.schemas.teachers import (
    PrimaryTeacher,
    SecondaryTeacher,
    CreatePrimaryTeacher,
    UpdatePrimaryTeacher,
    CreateSecondaryTeacher,
    UpdateSecondaryTeacher,
)

__all__ = [
    "get_primary_teacher",
    "create_primary_teacher",
    "update_primary_teacher",
    "delete_primary_teacher",
    "get_secondary_teacher",
    "create_secondary_teacher",
    "update_secondary_teacher",
    "delete_secondary_teacher",
]

primary_router = APIRouter(
    tags=["Primary Teachers 👨‍🏫 🏫"], prefix="/teachers/primary"
)
secondary_router = APIRouter(
    tags=["Secondary Teachers 👨‍🏫 🏨"], prefix="/teachers/secondary"
)
all_router = APIRouter(tags=["All Teachers 👨‍🏫"], prefix="/teachers/all")


@primary_router.get("/", status_code=200)
def get_primary_teacher(teacher_id: Optional[int] = None):
    try:
        result = pull_teachers_from_db(teacher_id=teacher_id, is_primary=True)
        if not result:
            return []
        return result
    except Exception as e:
        print(e)
        if result is None:
            detail = "Could not retrieve primary teachers in database!"
        else:
            detail = f"Primary teacher with ID `{teacher_id}` not in database!"

            raise HTTPException(status_code=404, detail=detail)


@primary_router.post("/", status_code=202, response_model=List[TeacherType])
def create_primary_teacher(teacher: CreatePrimaryTeacher):
    try:
        teacher_dict = teacher.dict()
        teacher_dict = push_teacher_to_db(teacher_dict=teacher_dict, is_primary=True)
        return [PrimaryTeacher(**teacher_dict)]
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Could not create new primary teacher!"
        )


@primary_router.put(
    "/{teacher_id}", status_code=202, response_model=List[DisplayPrimaryTeacher]
)
def update_primary_teacher(teacher_id: int, teacher: UpdatePrimaryTeacher):
    try:
        teacher_dict = teacher.dict()
        teacher_dict["id"] = teacher_id

        teacher_dict = update_teacher_in_db(teacher_dict=teacher_dict, is_primary=True)

        if not teacher_dict:
            raise HTTPException(
                status_code=404,
                detail=f"Primary teacher with ID `{teacher_id}` not in database!",
            )
        return teacher_dict
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail=f"Primary teacher with ID `{teacher_id}` not in database!",
        )


@primary_router.delete("/{teacher_id}", response_model=List[DisplayPrimaryTeacher])
def delete_primary_teacher(teacher_id: int):
    try:
        teacher_dict = delete_teacher_from_db(teacher_id=teacher_id, is_primary=True)
        if not teacher_dict:
            raise HTTPException(
                status_code=404,
                detail=f"Primary teacher with ID `{teacher_id}` not in database!",
            )
        return teacher_dict
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail=f"Primary teacher with ID `{teacher_id}` not in database!",
        )


@secondary_router.get("/", status_code=200, response_model=List[TeacherType])
def get_secondary_teacher(teacher_id: Optional[int] = None):
    try:
        result = pull_teachers_from_db(teacher_id=teacher_id, is_primary=False)
        return result
    except Exception as e:
        print(e)
        if result is None:
            detail = "Could not retrieve secondary teachers in database!"
        else:
            detail = f"Secondary teacher with ID `{teacher_id}` not in database!"

            raise HTTPException(status_code=404, detail=detail)


@secondary_router.post("/", status_code=202, response_model=List[TeacherType])
def create_secondary_teacher(teacher: CreateSecondaryTeacher):
    try:
        teacher_dict = teacher.dict()
        teacher_dict = push_teacher_to_db(teacher_dict=teacher_dict, is_primary=False)
        return [SecondaryTeacher(**teacher_dict)]
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Could not create new secondary teacher!"
        )


@secondary_router.put(
    "/{teacher_id}", status_code=202, response_model=List[DisplaySecondaryTeacher]
)
def update_secondary_teacher(teacher_id: int, teacher: UpdateSecondaryTeacher):
    try:
        teacher_dict = teacher.dict()
        teacher_dict["id"] = teacher_id

        teacher_dict = update_teacher_in_db(teacher_dict=teacher_dict, is_primary=False)

        if not teacher_dict:
            raise HTTPException(
                status_code=404,
                detail=f"Secondary teacher with ID `{teacher_id}` not in database!",
            )
        return teacher_dict
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail=f"Secondary teacher with ID `{teacher_id}` not in database!",
        )


@secondary_router.delete("/{teacher_id}", response_model=List[DisplaySecondaryTeacher])
def delete_secondary_teacher(teacher_id: int):
    try:
        teacher_dict = delete_teacher_from_db(teacher_id=teacher_id, is_primary=False)
        if not teacher_dict:
            raise HTTPException(
                status_code=404,
                detail=f"Secondary teacher with ID `{teacher_id}` not in database!",
            )
        return teacher_dict
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail=f"Secondary teacher with ID `{teacher_id}` not in database!",
        )


@all_router.get("/", response_model=Dict[str, List[TeacherType]], status_code=200)
def get_all_teachers():
    primary_teachers = pull_teachers_from_db(teacher_id=None, is_primary=True)
    secondary_teachers = pull_teachers_from_db(teacher_id=None, is_primary=False)

    return {
        "primary": [PrimaryTeacher(**teacher) for teacher in primary_teachers],
        "secondary": [SecondaryTeacher(**teacher) for teacher in secondary_teachers],
    }
