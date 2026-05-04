import os
import urllib.parse
from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


_engine: Engine | None = None
_session_local: sessionmaker[Session] | None = None


def get_engine() -> Engine:
    global _engine, _session_local
    if _engine is None:
        password: str = os.environ["MSSQL_SA_PASSWORD"]
        odbc_str: str = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=tcp:sqldbrk01.database.windows.net,1433;"
            "Database=sqldbrk01;"
            f"Uid=sqladmin;Pwd={password};"
            "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        )
        url: str = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(odbc_str)
        _engine = create_engine(url, echo=False)
        _session_local = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _engine


def get_db() -> Generator[Session, None, None]:
    get_engine()
    db: Session = _session_local()  # type: ignore[misc]
    try:
        yield db
    finally:
        db.close()
