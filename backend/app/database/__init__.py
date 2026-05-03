"""
Database module. It keeps persistence details separate from route handlers so the API code stays easier to explain and maintain. This file handles the   init   part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

# Database package
from . import models
from . import crud
from .session import get_session, engine

__all__ = ["models", "crud", "get_session", "engine"]


