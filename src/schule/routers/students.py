# -*- coding: utf-8 -*-

import uuid

from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException

from schule.utils import (
    delete_student_from_db,
    pull_students_from_db,
    push_student_to_db,
    push_guardian_to_db,
    pull_guardians_from_db,
)

from schule.schemas import StudentType, EntityType
from schule.schemas.guardians import Guardian
from schule.schemas.students import (
    PrimaryStudent,
    SecondaryStudent,
    CreatePrimaryStudent,
    CreateSecondaryStudent,
)

__all__ = [
    "get_primary_students",
    "create_primary_student",
    "delete_primary_student",
    "get_secondary_students",
    "create_secondary_student",
    "delete_secondary_student",
    "get_all_students",
]


primary_router = APIRouter(tags=["Primary Students 🎒🧒"], prefix="/students/primary")
secondary_router = APIRouter(
    tags=["Secondary Students 📜👩‍🎓"], prefix="/students/secondary"
)
all_router = APIRouter(tags=["All Students 🎒👩‍🎓"], prefix="/students/all")


@primary_router.get("/", response_model=List[StudentType])
def get_primary_students(student_id: Optional[str] = None):
    students_json = pull_students_from_db(student_id=student_id, is_primary=True)

    if students_json is None:
        raise HTTPException(
            status_code=404,
            detail=f"Primary student with ID `{student_id}` does not exist!",
        )

    return [PrimaryStudent(**student) for student in students_json]


@primary_router.post("/", response_model=Dict[str, List[EntityType]])
def create_primary_student(student: CreatePrimaryStudent):
    student_id = student.id
    guardian_id = student.guardian_id

    print(student)

    if student_id is None:
        student_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_DNS,
                f"{student.first_name}.{student.last_name}.{student.grade}",
            )
        )
    else:
        student_dict = pull_students_from_db(student_id=student_id, is_primary=True)
        if student_dict:
            raise HTTPException(
                status_code=404,
                detail=f"Primary student with ID `{student_id}` already exists!",
            )

    if guardian_id is None:
        guardian_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_DNS,
                f"{student.guardian_first_name}.{student.guardian_first_name}",
            )
        )
        guardian = Guardian(
            id=guardian_id,
            ward_ids=[student_id],
            first_name=student.guardian_first_name,
            last_name=student.guardian_last_name,
            email=student.guardian_email,
            password=student.guardian_password,
        )
    else:
        guardian = pull_guardians_from_db(guardian_id=guardian_id)

        if guardian:
            guardian = Guardian(**guardian[0])

            if guardian.ward_ids is None:
                guardian.ward_ids = [student_id]
            else:
                guardian.ward_ids += [student_id]
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Guardian with ID `{guardian_id}` not found in school database.",
            )

    primary_student = PrimaryStudent(
        id=student_id,
        guardian_id=guardian_id,
        first_name=student.first_name,
        last_name=student.last_name,
        grade=student.grade,
    )

    push_guardian_to_db(guardian.dict())
    push_student_to_db(primary_student.dict(), is_primary=True)

    return {"student": [primary_student], "guardian": [guardian]}


@primary_router.delete("/{student_id}", response_model=Dict[str, List[EntityType]])
def delete_primary_student(student_id: str):
    student_data, guardian_data = delete_student_from_db(
        student_id=student_id, is_primary=True
    )

    if not student_data:
        raise HTTPException(
            status_code=404,
            detail=f"Primary student with ID `{student_id}` does not exist!",
        )

    if guardian_data is not None:
        guardian_data = [Guardian(**guardian_data)]
    else:
        guardian_data = []

    return {
        "student": [PrimaryStudent(**student_data)],
        "guardian": guardian_data,
    }


@secondary_router.get("/", response_model=List[StudentType])
def get_secondary_students(student_id: Optional[str] = None):
    students_json = pull_students_from_db(student_id=student_id, is_primary=False)

    if students_json is None:
        raise HTTPException(
            status_code=404,
            detail=f"Secondary student with ID `{student_id}` does not exist!",
        )

    return [SecondaryStudent(**student) for student in students_json]


@secondary_router.post("/", response_model=Dict[str, List[EntityType]])
def create_secondary_student(student: CreateSecondaryStudent):
    student_id = student.id
    guardian_id = student.guardian_id

    if student_id is None:
        student_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_DNS,
                f"{student.first_name}.{student.last_name}.{student.grade}",
            )
        )
    else:
        try:
            student_dict = pull_students_from_db(
                student_id=student_id, is_primary=False
            )
            if student_dict:
                raise HTTPException(
                    status_code=404,
                    detail=f"Secondary student with ID `{student_id}` already exists!",
                )
        except:
            pass

    if guardian_id is None:
        guardian_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_DNS,
                f"{student.guardian_first_name}.{student.guardian_last_name}",
            )
        )
        guardian = Guardian(
            id=guardian_id,
            ward_ids=[student_id],
            first_name=student.guardian_first_name,
            last_name=student.guardian_last_name,
            email=student.guardian_email,
            password=student.guardian_password,
        )
    else:
        guardian = pull_guardians_from_db(guardian_id=guardian_id)

        if guardian:
            guardian = Guardian(**guardian[0])

            if guardian.ward_ids is None:
                guardian.ward_ids = [student_id]
            else:
                guardian.ward_ids += [student_id]
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Guardian with ID `{guardian_id}` not found in school database.",
            )

    secondary_student = SecondaryStudent(
        id=student_id,
        guardian_id=guardian_id,
        first_name=student.first_name,
        last_name=student.last_name,
        grade=student.grade,
        email=student.email,
        password=student.password,
    )

    push_guardian_to_db(guardian.dict())
    push_student_to_db(secondary_student.dict(), is_primary=False)

    return {"student": [secondary_student], "guardian": [guardian]}


@secondary_router.delete("/{student_id}", response_model=Dict[str, List[EntityType]])
def delete_secondary_student(student_id: str):
    student_data, guardian_data = delete_student_from_db(
        student_id=student_id, is_primary=False
    )

    if not student_data:
        raise HTTPException(
            status_code=404,
            detail=f"Secondary student with ID `{student_id}` does not exist!",
        )

    if guardian_data is not None:
        guardian_data = [Guardian(**guardian_data)]
    else:
        guardian_data = []

    return {
        "student": [SecondaryStudent(**student_data)],
        "guardian": guardian_data,
    }


@all_router.get("/", response_model=Dict[str, List[StudentType]])
def get_all_students():
    primary_students = pull_students_from_db(student_id=None, is_primary=True)
    secondary_students = pull_students_from_db(student_id=None, is_primary=False)

    return {
        "primary": [PrimaryStudent(**student) for student in primary_students],
        "secondary": [SecondaryStudent(**student) for student in secondary_students],
    }
