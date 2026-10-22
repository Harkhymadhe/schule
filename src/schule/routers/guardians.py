# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Union
from fastapi import APIRouter, HTTPException

from schule.utils import (
    delete_guardian_from_db,
    pull_guardians_from_db,
    pull_students_by_guardian_from_db,
)

from schule.schemas import GuardianType, EntityMap
from schule.schemas.guardians import Guardian
from schule.schemas.students import PrimaryStudent, SecondaryStudent

__all__ = [
    "get_guardians",
    "get_guardian_wards",
    "delete_guardian",
]

router = APIRouter(tags=["Guardians 💂‍♀️"], prefix="/guardians")


@router.get("/", response_model=List[GuardianType])
def get_guardians(guardian_id: Optional[str] = None):
    try:
        guardians_json = pull_guardians_from_db(guardian_id=guardian_id)

        if guardians_json:
            return [Guardian(**guardian) for guardian in guardians_json]
        else:
            return []

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=404, detail=f"Guardian with ID {guardian_id} does not exist!"
        )


@router.get(
    "/{guardian_id}/wards", response_model=Dict[str, Union[GuardianType, EntityMap]]
)
def get_guardian_wards(guardian_id: str):
    try:
        guardian_data = pull_guardians_from_db(guardian_id=guardian_id)

        if not guardian_data:
            raise HTTPException(
                status_code=404,
                detail=f"Database does not contain guardian with ID `{guardian_id}`!",
            )

        guardian_data = guardian_data[0]

        primary_students = pull_students_by_guardian_from_db(
            guardian_id=guardian_id, is_primary=True
        )
        secondary_students = pull_students_by_guardian_from_db(
            guardian_id=guardian_id, is_primary=False
        )

        return {
            "guardian": Guardian(**guardian_data),
            "wards": {
                "primary": [PrimaryStudent(**data) for data in primary_students],
                "secondary": [SecondaryStudent(**data) for data in secondary_students],
            },
        }
    except:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot pull wards for guardian `{guardian_id}` at this time.",
        )


@router.delete(
    "/{guardian_id}", response_model=Dict[str, Union[List[GuardianType], EntityMap]]
)
def delete_guardian(guardian_id: str):
    try:
        return delete_guardian_from_db(guardian_id=guardian_id, delete_students=True)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=404, detail=f"Guardian with ID `{guardian_id}` does not exist!"
        )
