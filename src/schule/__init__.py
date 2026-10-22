# -*- coding: utf-8 -*-

from . import routers
from . import schemas
from . import utils

from .utils import database_setup

database_setup()

__all__ = ["routers", "schemas", "utils"]
