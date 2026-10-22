# -*- coding: utf-8 -*-

"""Implemented API endpoints for school management system (SMS)"""

from fastapi import FastAPI

from schule.routers import auth, guardians, students, subjects, teachers

app = FastAPI()

# Authentication router
app.include_router(auth.router)

# Guardian routers
app.include_router(guardians.router)

# Student routers
app.include_router(students.primary_router)
app.include_router(students.secondary_router)
app.include_router(students.all_router)

# Subject routers
app.include_router(subjects.primary_router)
app.include_router(subjects.secondary_router)
app.include_router(subjects.all_router)

# Teacher routers
app.include_router(teachers.primary_router)
app.include_router(teachers.secondary_router)
app.include_router(teachers.all_router)
