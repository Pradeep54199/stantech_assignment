from app.core.settings import get_settings

print(get_settings())

from app.core.db import get_db
from sqlalchemy import text

with get_db() as db:
    # result = db.execute(text("show databases;"))

    result = db.execute(text("SELECT current_database();"))
    for row in result:
        print(row)

