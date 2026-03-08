from sqlmodel import Session, create_engine
from typing import Generator, Annotated, cast
from pathlib import Path
from fastapi import Depends

from dotenv import load_dotenv
import os

load_dotenv()

BASE_PATH = Path(__file__).resolve().parent.parent
LOCAL_DB_PATH = BASE_PATH / "local.db"

SQLITE_URL = "sqlite:///local.db"
CONNECT_ARGS = { "check_same_thread": False }

SUPABASE_URL_PROD: str = cast(str, os.environ.get("SUPABASE_URL"))

engine = create_engine(url=SUPABASE_URL_PROD, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]