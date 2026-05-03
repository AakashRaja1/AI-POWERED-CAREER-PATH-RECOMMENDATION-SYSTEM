"""
FastAPI router module. It groups related endpoints so each feature has a clear backend boundary. This file handles the   init   part of the project.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

# Router package
from .items import router
