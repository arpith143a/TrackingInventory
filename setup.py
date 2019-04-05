from models import Base, DATABASE_URI
from sqlalchemy import create_engine

def setup(database_uri=DATABASE_URI, echo=True, **kwargs):
    engine = create_engine(database_uri, echo=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    setup()
