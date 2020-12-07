# ERAlchemy
# Github: https://github.com/Alexis-benoist/eralchemy
# Pypi: https://pypi.org/project/ERAlchemy/
import os
import sys
sys.path.append(os.getcwd())

from eralchemy import render_er
from app.core.config import settings

# Draw from database
render_er(settings.SQLALCHEMY_DATABASE_URI, 'docs/schemas/entity-relation_diagram.png')
