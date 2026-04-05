from app.database.db import engine, Base
from app.models.application import JobApplication

def init_db():
    Base.metadata.create_all(bind=engine)