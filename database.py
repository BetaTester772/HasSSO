from sqlmodel import SQLModel, create_engine, Session

# get database connection string from .env file
from starlette.config import Config

config = Config('.env')
database_connection_string = config('SQLALCHEMY_DATABASE_URL')

engine_url = create_engine(database_connection_string, echo=False)


def conn():
    SQLModel.metadata.create_all(engine_url)


# Session 사용 후 자동으로 종료
def get_session():
    with Session(engine_url) as session:
        yield session
