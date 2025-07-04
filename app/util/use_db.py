from ..db.database import SessionLocal

# use DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()