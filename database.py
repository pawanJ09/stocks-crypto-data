from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine(f'postgresql+psycopg2://{os.environ["STOCKS_USER"]}'
                       f':{os.environ["STOCKS_PASSWORD"]}@{os.environ["STOCKS_DB_HOST"]}/stocksdb',
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import model
    Base.metadata.create_all(bind=engine)
    print("Database Initiated")