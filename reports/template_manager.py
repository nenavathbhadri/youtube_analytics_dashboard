from sqlalchemy import text
from database.db import get_engine
import json

engine = get_engine()


def save_template(name, sections):

    query = text("""
        INSERT INTO report_templates (template_name, sections)
        VALUES (:name, :sections)
    """)

    with engine.connect() as conn:
        conn.execute(query, {
            "name": name,
            "sections": json.dumps(sections)
        })
        conn.commit()


def load_templates():

    query = text("SELECT * FROM report_templates")

    with engine.connect() as conn:
        return conn.execute(query).fetchall()