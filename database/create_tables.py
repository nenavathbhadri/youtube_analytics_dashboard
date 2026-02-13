import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from database.db import get_engine
from database.models import Base

engine = get_engine()

print("Creating tables...")

Base.metadata.create_all(engine)

print("Tables created successfully!")
