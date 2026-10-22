# -*- coding: utf-8 -*-

from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException

from schule.utils import (
    delete_subject_from_db,
    pull_subjects_from_db,
    push_subject_to_db,
    update_subject_in_db,
)

from schule.schemas import SubjectType
from schule.schemas.subjects import (
    PrimarySubject,
    SecondarySubject,
    CreatePrimarySubject,
    CreateSecondarySubject,
    UpdatePrimarySubject,
    UpdateSecondarySubject,
)

__all__ = [
    "get_primary_subjects",
    "create_primary_subject",
    "delete_primary_subject",
    "get_secondary_subjects",
    "create_secondary_subject",
    "delete_secondary_subject",
    "get_all_subjects",
]

primary_router = APIRouter(tags=["Primary Subjects 🔡"], prefix="/subjects/primary")
secondary_router = APIRouter(
    tags=["Secondary Subjects 📖"], prefix="/subjects/secondary"
)
all_router = APIRouter(tags=["All Subjects 🔡📖"], prefix="/subjects/all")


@primary_router.get("/", response_model=List[SubjectType])
def get_primary_subjects(subject_id: Optional[int] = None):
    try:
        subjects = pull_subjects_from_db(subject_id=subject_id, is_primary=True)
        return [PrimarySubject(**data) for data in subjects]
    except:
        raise HTTPException(
            status_code=404,
            detail=f"Primary school subject with ID `{subject_id}` does not exist!",
        )


@primary_router.post("/", response_model=List[PrimarySubject])
def create_primary_subject(subject: CreatePrimarySubject):
    subject_data = subject.dict()
    subject_data = push_subject_to_db(subject_data, is_primary=True)

    return [PrimarySubject(**subject_data)]


@primary_router.put(
    "/{subject_id}", response_model=List[PrimarySubject], status_code=202
)
def update_primary_subject(subject_id: int, subject: UpdatePrimarySubject):
    try:
        subject_dict = subject.dict()
        subject_dict["id"] = subject_id

        return update_subject_in_db(subject_dict=subject_dict, is_primary=True)
    except:
        raise HTTPException(
            status_code=404,
            detail=f"Primary school subject with ID `{subject.id}` could not be updated!",
        )


@primary_router.delete("/{subject_id}", response_model=List[PrimarySubject])
def delete_primary_subject(subject_id: int):
    subject_data = delete_subject_from_db(subject_id=subject_id, is_primary=True)

    return [PrimarySubject(**data) for data in subject_data]


@secondary_router.get("/", response_model=List[SubjectType])
def get_secondary_subjects(subject_id: Optional[int] = None):
    try:
        subjects = pull_subjects_from_db(subject_id=subject_id, is_primary=False)
        return [SecondarySubject(**data) for data in subjects]
    except:
        raise HTTPException(
            status_code=404,
            detail=f"Secondary school subject with ID `{subject_id}` does not exist!",
        )


@secondary_router.post("/", response_model=List[SecondarySubject])
def create_secondary_subject(subject: CreateSecondarySubject):
    subject_data = subject.dict()
    subject_data = push_subject_to_db(subject_data, is_primary=False)

    return [SecondarySubject(**subject_data)]


@secondary_router.put(
    "/{subject_id}", response_model=List[SecondarySubject], status_code=202
)
def update_secondary_subject(subject_id: int, subject: UpdateSecondarySubject):
    try:
        subject_dict = subject.dict()
        subject_dict["id"] = subject_id

        return update_subject_in_db(subject_dict=subject_dict, is_primary=False)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail=f"Secondary school subject with ID `{subject.id}` could not be updated!",
        )


@secondary_router.delete("/{subject_id}", response_model=List[SecondarySubject])
def delete_secondary_subject(subject_id: int):
    subject_data = delete_subject_from_db(subject_id=subject_id, is_primary=False)

    return [SecondarySubject(**data) for data in subject_data]


@all_router.get("/", response_model=Dict[str, List[SubjectType]], status_code=200)
def get_all_subjects():
    primary_subjects = pull_subjects_from_db(subject_id=None, is_primary=True)
    secondary_subjects = pull_subjects_from_db(subject_id=None, is_primary=False)

    return {
        "primary": [PrimarySubject(**subject) for subject in primary_subjects],
        "secondary": [SecondarySubject(**subject) for subject in secondary_subjects],
    }
