from sqlmodel import SQLModel, create_engine, Session

database_file = 'my_website.db'
database_connection_string = f"sqlite:///{database_file}"

engine_url = create_engine(database_connection_string, echo=True)


def conn():
    SQLModel.metadata.create_all(engine_url)


# Session 사용 후 자동으로 종료
def get_session():
    with Session(engine_url) as session:
        yield session
