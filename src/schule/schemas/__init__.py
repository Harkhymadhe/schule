# -*- coding: utf-8 -*-

from typing import Dict, List, Union

from .auth import User
from .guardians import DisplayGuardian
from .students import DisplayPrimaryStudent, DisplaySecondaryStudent
from .subjects import PrimarySubject, SecondarySubject
from .teachers import DisplayPrimaryTeacher, DisplaySecondaryTeacher

__all__ = [
    "UserType",
    "StudentType",
    "GuardianType",
    "SubjectType",
    "EntityType",
    "StudentMap",
    "GuardianMap",
    "SubjectMap",
    "EntityMap",
]


UserType = User
StudentType = Union[DisplayPrimaryStudent, DisplaySecondaryStudent]
GuardianType = DisplayGuardian
SubjectType = Union[PrimarySubject, SecondarySubject]
TeacherType = Union[DisplayPrimaryTeacher, DisplaySecondaryTeacher]
EntityType = Union[GuardianType, StudentType, TeacherType]

UserType = Dict[str, List[UserType]]
StudentMap = Dict[str, List[StudentType]]
GuardianMap = Dict[str, List[GuardianType]]
SubjectMap = Dict[str, List[SubjectType]]
TeacherMap = Dict[str, List[TeacherType]]
EntityMap = Dict[str, Union[EntityType, List[EntityType]]]
