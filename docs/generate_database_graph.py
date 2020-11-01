# ERAlchemy
# Github: https://github.com/Alexis-benoist/eralchemy
# Pypi: https://pypi.org/project/ERAlchemy/
from eralchemy import render_er

# Draw from database
render_er("sqlite:///./sql_app.db", 'docs/schemas/erd_from_sqlite.png')
