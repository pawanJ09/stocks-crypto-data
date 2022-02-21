from database import Base, db_session
from sqlalchemy import Column, Integer, String


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
        return cls.query.filter(StocksCodeModel.name == name).first()

    def save_to_db(self):
        db_session.add(self)
        db_session.commit()

    def delete_from_db(self):
        db_session.delete(self)
        db_session.commit()

