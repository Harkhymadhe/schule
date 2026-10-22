# -*- coding: utf-8 -*-

"""Utilities for storing and extracting user data as created from API endpoints."""

import os
import json
import sqlite3

from typing import Any, Dict, List, Tuple, Union, Optional

__all__ = [
    "DATABASE_PATH",
    "DATABASE_SCRIPT_PATH",
    "_prepare_guardian_value_for_db",
    "_postprocess_guardian_values_from_db",
    "database_setup",
    "authenticate_user_id",
    "pull_guardians_from_db",
    "pull_students_from_db",
    "pull_students_by_guardian_from_db",
    "push_guardian_to_db",
    "push_student_to_db",
    "push_subject_to_db",
    "pull_subjects_from_db",
    "delete_subject_from_db",
    "update_subject_in_db",
]

DATABASE_PATH: str = os.path.join(
    os.path.dirname(__file__), "database", "database", "school_database.db"
)
DATABASE_SCRIPT_PATH: str = os.path.join(
    os.path.dirname(__file__), "database", "src", "db_create.sql"
)


def _prepare_guardian_value_for_db(guardian_value: Any) -> str:
    if isinstance(guardian_value, (int, float)):
        return f"{guardian_value}"
    elif isinstance(guardian_value, list):
        return f"'{json.dumps(guardian_value)}'"
    elif guardian_value is None:
        return "NULL"
    else:
        return f"'{guardian_value}'"


def _postprocess_guardian_values_from_db(
    columns: List[str], row: Tuple[Union[str, int, float]]
) -> Dict[str, Union[str, int, float]]:
    values = dict(zip(columns, row))
    ward_ids = values["ward_ids"]
    values["ward_ids"] = [] if ward_ids.lower() == "null" else json.loads(ward_ids)

    return values


def database_setup():
    with open(DATABASE_SCRIPT_PATH, "r") as f:
        script_string: str = f.read()

        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.executescript(script_string)

            cursor = conn.cursor()
            cursor.execute("""SELECT name FROM sqlite_master WHERE type = 'table';""")
            rows = cursor.fetchall()

            db_tables = [row[0] for row in rows]

            tables = "".join([f"  - {name}\n" for name in db_tables])
            text = f"\nThe tables in the database are:\n\n{tables}"

            print(text)


def authenticate_user_id(email: str, password: str, is_guardian: bool):
    TABLE_NAME: str = "guardians" if is_guardian else "secondary_students"

    QUERY: str = f"""SELECT * FROM {TABLE_NAME} WHERE email = '{email}' AND password = '{password}';"""

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(QUERY)
        result = cursor.fetchone()

    return bool(result)


def pull_guardians_from_db(guardian_id: Optional[str] = None):
    TABLE_NAME: str = "guardians"
    QUERY: str = f"""SELECT * FROM {TABLE_NAME}"""

    if guardian_id is not None:
        QUERY: str = f"""{QUERY} WHERE id = '{guardian_id}';"""
    else:
        QUERY: str = f"""{QUERY};"""

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(QUERY)

        columns = [c[0] for c in cursor.description]

        guardian_data = [
            _postprocess_guardian_values_from_db(columns, row)
            for row in cursor.fetchall()
        ]

    return guardian_data


def pull_students_from_db(is_primary: bool, student_id: Optional[str] = None):
    TABLE_NAME: str = "primary_students" if is_primary else "secondary_students"

    QUERY: str = f"""SELECT * FROM {TABLE_NAME}"""

    if student_id:
        QUERY: str = f"""{QUERY} WHERE id = '{student_id}';"""
    else:
        QUERY: str = f"""{QUERY};"""

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(QUERY)

        columns = [c[0] for c in cursor.description]

        student_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return student_data


def pull_students_by_guardian_from_db(
    is_primary: bool, guardian_id: Optional[str] = None
):
    TABLE_NAME: str = "primary_students" if is_primary else "secondary_students"

    QUERY: str = f"""SELECT * FROM {TABLE_NAME}"""

    if guardian_id:
        QUERY: str = f"""{QUERY} WHERE guardian_id = '{guardian_id}';"""
    else:
        QUERY: str = f"""{QUERY};"""

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(QUERY)

        columns = [c[0] for c in cursor.description]

        student_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return student_data


def delete_student_from_db(student_id: str, is_primary: bool):
    STUDENT_TABLE: str = "primary_students" if is_primary else "secondary_students"
    GUARDIAN_TABLE: str = "guardians"

    SELECT_QUERY = f"""SELECT * FROM {STUDENT_TABLE} WHERE id = '{student_id}';"""
    DELETE_QUERY = f"""DELETE FROM {STUDENT_TABLE} WHERE id = '{student_id}';"""

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        # Select student data to delete first

        cursor.execute(SELECT_QUERY)

        columns = [c[0] for c in cursor.description]

        student_data = [dict(zip(columns, row)) for row in cursor.fetchall()][0]

        # Delete student data
        cursor.execute(DELETE_QUERY)
        conn.commit()

        print(f"\nStudent to delete: {student_data}")

        # Get student guardian
        guardian_id = student_data["guardian_id"]
        guardian_data = pull_guardians_from_db(guardian_id=guardian_id)[0]

        print(f"Guardian of student to delete ({type(guardian_data)}): {guardian_data}")

        ward_ids = guardian_data["ward_ids"]
        ward_ids.remove(student_id)

        print(f"Present wards ({type(ward_ids)}): {ward_ids}")

        if not ward_ids:
            print(f"Deleting guardian with ID `{guardian_id}` ...")
            _ = delete_guardian_from_db(guardian_id=guardian_id, delete_students=False)
        else:
            print(f"Updating wards for guardian with ID `{guardian_id}` ...")

            ward_ids = _prepare_guardian_value_for_db(ward_ids)

            UPDATE_QUERY: str = f"""UPDATE {GUARDIAN_TABLE} SET ward_ids = {ward_ids} WHERE id = '{guardian_id}';"""
            cursor.execute(UPDATE_QUERY)

            conn.commit()

    return student_data, guardian_data


def push_guardian_to_db(guardian_dict):
    guardian_id = guardian_dict["id"]

    TABLE_NAME: str = "guardians"
    QUERY: str = f"""SELECT * FROM {TABLE_NAME} WHERE id = '{guardian_id}';"""

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(QUERY)

        results = cursor.fetchall()

        if results:
            QUERY: str = """UPDATE {TABLE_NAME} SET {COLUMN} = {VALUE} WHERE id = '{GUARDIAN_ID}'"""
            columns = [c[0] for c in cursor.description]

            update_queries = [
                QUERY.format(
                    TABLE_NAME=TABLE_NAME,
                    COLUMN=k,
                    VALUE=_prepare_guardian_value_for_db(guardian_dict[k]),
                    GUARDIAN_ID=guardian_id,
                )
                for k in columns
                if k != "id"
            ]

            conn.executescript(f"""{";\n".join(update_queries)}""")
            conn.commit()
            return

        keys = list(guardian_dict.keys())
        values = [guardian_dict[k] for k in keys]

        COLUMNS: str = ", ".join(keys)
        VALUES: str = ", ".join([_prepare_guardian_value_for_db(v) for v in values])

        INSERT_QUERY: str = (
            f"""INSERT INTO {TABLE_NAME} ({COLUMNS}) VALUES ({VALUES});"""
        )

        cursor.execute(INSERT_QUERY)

        conn.commit()

    return


def push_student_to_db(student_dict, is_primary: bool):
    student_id = student_dict["id"]

    TABLE_NAME: str = "primary_students" if is_primary else "secondary_students"
    QUERY: str = f"""SELECT * FROM {TABLE_NAME} WHERE id = '{student_id}';"""

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(QUERY)

        results = cursor.fetchall()

        if results:
            QUERY: str = """UPDATE {TABLE_NAME} SET {COLUMN} = {VALUE} WHERE id = '{STUDENT_ID}'"""
            columns = [c[0] for c in cursor.description]

            update_queries = [
                QUERY.format(
                    TABLE_NAME=TABLE_NAME,
                    COLUMN=k,
                    VALUE=f"'{student_dict[k]}"
                    if isinstance(student_dict[k], str)
                    else f"{student_dict[k]}",
                    STUDENT_ID=student_id,
                )
                for k in columns
                if k != "id"
            ]

            conn.executescript(f"""{";\n".join(update_queries)}""")
            conn.commit()
            return

        keys = list(student_dict.keys())
        values = [student_dict[k] for k in keys]

        COLUMNS: str = ", ".join([f"'{k}'" for k in keys])
        VALUES: str = ", ".join(
            [(f"'{v}'" if isinstance(v, str) else f"{v}") for v in values]
        )

        INSERT_QUERY: str = (
            f"""INSERT INTO {TABLE_NAME} ({COLUMNS}) VALUES ({VALUES});"""
        )

        cursor.execute(INSERT_QUERY)

        conn.commit()

    return


def delete_guardian_from_db(guardian_id: str, delete_students: bool = False):
    GUARDIAN_TABLE: str = "guardians"
    DELETE_QUERY: str = f"""DELETE FROM {GUARDIAN_TABLE} WHERE id = '{guardian_id}';"""

    def _delete_student_from_db(student_id: str):
        try:
            is_primary = True
            student, guardian = delete_student_from_db(
                student_id=student_id, is_primary=is_primary
            )
        except Exception as e:
            print(f"Exception in deleting students: {e}")
            is_primary = False
            student, guardian = delete_student_from_db(
                student_id=student_id, is_primary=is_primary
            )

        return student, guardian, is_primary

    def _pull_student_from_db(student_id: str):
        try:
            is_primary = True
            student = pull_students_from_db(
                student_id=student_id, is_primary=is_primary
            )
            student = student[0]
        except Exception as e:
            print(f"Exception in pulling students: {e}")
            is_primary = False
            student = pull_students_from_db(
                student_id=student_id, is_primary=is_primary
            )
            student = student[0]

        return student, is_primary

    # Connect to database
    with sqlite3.connect(DATABASE_PATH) as conn:
        # Check if guardian with guardian ID is in guardian table
        guardians = pull_guardians_from_db(guardian_id=guardian_id)

        # If not, ...
        if not guardians:
            # ... return an empty list of guardians
            return {"guardians": []}

        # else, select the first guardian (we only need one guardian with specified ID)

        guardian_data = guardians[0]

        print(guardian_data)

        # Instantiate Cursor object
        cursor = conn.cursor()

        # If we need to delete all students associated with guardian ID ...

        if delete_students:
            # NOTE: OPTION 1
            students: list = []

            for student_id in guardian_data["ward_ids"]:
                student, _, is_primary = _delete_student_from_db(student_id=student_id)
                students.append((student, is_primary))

            # NOTE: OPTION 2
            # students = [_pull_student_from_db(student_id) for student_id in guardian_data["ward_ids"]]

        # Execute guardian delete query
        cursor.execute(DELETE_QUERY)

        # Commit all database changes.
        conn.commit()

    return (
        {"guardian": guardians}
        if not delete_students
        else {
            "guardian": guardians,
            "students": {
                "primary": [data for data, status in students if status],
                "secondary": [data for data, status in students if not status],
            },
        }
    )


def push_subject_to_db(subject_dict, is_primary: bool):
    TABLE_NAME: str = "primary_subjects" if is_primary else "secondary_subjects"

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        ID = len(pull_subjects_from_db(is_primary=is_primary)) + 1
        subject_dict["id"] = ID

        print(ID)

        COLUMNS = list(subject_dict.keys())
        VALUES = [_prepare_guardian_value_for_db(subject_dict[k]) for k in COLUMNS]

        COLUMNS = ", ".join(COLUMNS)
        VALUES = ", ".join(VALUES)

        INSERT_QUERY: str = (
            f"""INSERT INTO {TABLE_NAME} ({COLUMNS}) VALUES ({VALUES});"""
        )

        cursor.execute(INSERT_QUERY)
        conn.commit()

        print("Subject successfully pushed!")

    return subject_dict


def pull_subjects_from_db(is_primary: bool, subject_id: Optional[int] = None):
    TABLE_NAME: str = "primary_subjects" if is_primary else "secondary_subjects"

    with sqlite3.connect(DATABASE_PATH) as conn:
        QUERY: str = f"""SELECT * FROM {TABLE_NAME}"""

        if subject_id:
            QUERY: str = f"""{QUERY} WHERE id = {subject_id};"""
        else:
            QUERY: str = f"""{QUERY};"""

        cursor = conn.cursor()

        cursor.execute(QUERY)

        columns = [column_info[0] for column_info in cursor.description]
        subject_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    print(subject_data)

    return subject_data


def delete_subject_from_db(subject_id: int, is_primary: bool):
    TABLE_NAME: str = "primary_subjects" if is_primary else "secondary_subjects"
    QUERY: str = f"""DELETE FROM {TABLE_NAME} WHERE id = {subject_id};"""

    subjects = pull_subjects_from_db(subject_id=subject_id, is_primary=is_primary)

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(QUERY)
        conn.commit()

    return subjects


def update_subject_in_db(subject_dict, is_primary: bool):
    TABLE_NAME: str = "primary_subjects" if is_primary else "secondary_subjects"
    ID: int = subject_dict["id"]

    subject_dict = {k: v for k, v in subject_dict.items() if v is not None}
    subjects = pull_subjects_from_db(subject_id=ID, is_primary=is_primary)

    if len(subject_dict) == 1:
        return subjects

    with sqlite3.connect(DATABASE_PATH) as conn:
        COL_VALS = ", ".join(
            [
                f"{col} = {_prepare_guardian_value_for_db(subject_dict[col])}"
                for col in subject_dict
                if col != "id"
            ]
        )
        QUERY: str = f"""UPDATE {TABLE_NAME} SET {COL_VALS} WHERE id = {ID};"""

        print(QUERY)

        cursor = conn.cursor()

        cursor.execute(QUERY)
        conn.commit()

    return pull_subjects_from_db(subject_id=ID, is_primary=is_primary)


def push_teacher_to_db(teacher_dict, is_primary: bool):
    TABLE_NAME: str = "primary_teachers" if is_primary else "secondary_teachers"

    COLUMNS = list(teacher_dict.keys())
    VALUES = [_prepare_guardian_value_for_db(teacher_dict[k]) for k in teacher_dict]

    COLUMNS = ", ".join(COLUMNS)
    VALUES = ", ".join(VALUES)

    with sqlite3.connect(DATABASE_PATH) as conn:
        QUERY: str = f"""INSERT INTO {TABLE_NAME} ({COLUMNS}) VALUES ({VALUES});"""

        cursor = conn.cursor()

        cursor.execute(QUERY)
        conn.commit()

    ID = len(pull_teachers_from_db(is_primary=is_primary))
    teacher_dict["id"] = ID

    return teacher_dict


def pull_teachers_from_db(is_primary: bool, teacher_id: Optional[int] = None):
    TABLE_NAME: str = "primary_teachers" if is_primary else "secondary_teachers"

    with sqlite3.connect(DATABASE_PATH) as conn:
        QUERY: str = f"""SELECT * FROM {TABLE_NAME}"""

        if teacher_id is None:
            QUERY = f"""{QUERY};"""
        else:
            QUERY = f"""{QUERY} WHERE id = {teacher_id};"""

        cursor = conn.cursor()

        cursor.execute(QUERY)

        rows = cursor.fetchall()
        column_names = [c[0] for c in cursor.description]

    if not rows:
        return []

    return [dict(zip(column_names, row)) for row in rows]


def delete_teacher_from_db(teacher_id: int, is_primary: bool):
    TABLE_NAME: str = "primary_teachers" if is_primary else "secondary_teachers"

    teacher_dict = pull_teachers_from_db(teacher_id=teacher_id, is_primary=is_primary)

    with sqlite3.connect(DATABASE_PATH) as conn:
        QUERY: str = f"""DELETE FROM {TABLE_NAME} WHERE id = {teacher_id};"""

        cursor = conn.cursor()

        cursor.execute(QUERY)
        conn.commit()

    return teacher_dict


def update_teacher_in_db(teacher_dict: dict, is_primary: bool):
    teacher_dict = {k: v for k, v in teacher_dict.items() if v is not None}
    teacher_id = teacher_dict.pop("id")

    if len(teacher_dict) == 0:
        teacher_info = pull_teachers_from_db(
            teacher_id=teacher_id, is_primary=is_primary
        )
        return teacher_info

    with sqlite3.connect(DATABASE_PATH) as conn:
        TABLE_NAME: str = "primary_teachers" if is_primary else "secondary_teachers"
        UPDATES: str = ", ".join(
            [
                f"""{col} = {_prepare_guardian_value_for_db(val)}"""
                for col, val in teacher_dict.items()
            ]
        )
        QUERY: str = f"""UPDATE {TABLE_NAME} SET {UPDATES} WHERE id = {teacher_id};"""

        cursor = conn.cursor()

        cursor.execute(QUERY)
        conn.commit()

    teacher_info = pull_teachers_from_db(teacher_id=teacher_id, is_primary=is_primary)
    return teacher_info
