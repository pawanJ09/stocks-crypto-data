from database import Base
from sqlalchemy import Column, Integer, String
from database import db_session


class StocksCodeModel(Base):

    __tablename__ = 'stocks_code'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    code = Column(String(10), nullable=False)

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def json(self):
        return {"id": self.id, "name": self.name, "code": self.code}

    def __repr__(self):
        return f"StocksCodeModel(id={self.id!r}, name={self.name!r}, code={self.code!r})"

    @classmethod
    def find_by_name(cls, name):
        return db_session.query(StocksCodeModel).filter(StocksCodeModel.name == name).first()

