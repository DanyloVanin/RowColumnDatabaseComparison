from decouple import config
from sqlalchemy.engine import create_engine
import cx_Oracle
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

oracle_user = config("ORACLE_USER")
oracle_password = config("ORACLE_PASSWORD")
oracle_dsn = config("ORACLE_DSN")

cx_Oracle.init_oracle_client(lib_dir=r"C:\\Users\\danyl\\Oracle\\instantclient_21_7")

engine = create_engine(f'oracle://{oracle_user}:{oracle_password}@{oracle_dsn}/?encoding=UTF-8&nencoding=UTF-8', max_identifier_length=128)
#
# with engine.connect() as conn:
#     print(conn.scalar("select sysdate from dual"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()