from sqlmodel import Session, create_engine
from typing import Generator, Annotated
from pathlib import Path
from fastapi import Depends

BASE_PATH = Path(__file__).resolve().parent.parent
LOCAL_DB_PATH = BASE_PATH / "local.db"

SQLITE_URL = "sqlite:///local.db"
CONNECT_ARGS = { "check_same_thread": False }

engine = create_engine(url=SQLITE_URL, connect_args=CONNECT_ARGS)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]