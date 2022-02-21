from sqlalchemy import Column, Integer, Date, Numeric, delete
from sqlalchemy.exc import DataError, SQLAlchemyError, DBAPIError
from database import Base, db_session
from model.stockscode import StocksCodeModel
from datetime import datetime


class StockModel(Base):

    __tablename__ = "stock"
    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer)
    stock_date = Column(Date)
    open_val = Column(Numeric(precision=10))
    high_val = Column(Numeric(precision=10))
    low_val = Column(Numeric(precision=10))
    close_val = Column(Numeric(precision=10))
    adj_close_val = Column(Numeric(precision=10))
    volume = Column(Numeric(precision=20))

    def __init__(self, stock_code_id, *args):
        self.stock_id = stock_code_id
        self.stock_date = datetime.strptime(args[0][0], '%Y-%m-%d').date()
        self.open_val = float(args[0][1])
        self.high_val = float(args[0][2])
        self.low_val = float(args[0][3])
        self.close_val = float(args[0][4])
        self.adj_close_val = float(args[0][5])
        self.volume = float(args[0][6])

    def __str__(self):
        return f'{self.stock_id},{self.stock_date},{self.open_val},{self.high_val},' \
               f'{self.low_val}, {self.close_val},{self.adj_close_val},{self.volume}'

    def json(self):
        return {"id": self.id, "stock_id": self.stock_id,
                "stock_date": self.stock_date.strftime('%Y-%m-%d'),
                "open_val": float(self.open_val), "high_val": float(self.high_val),
                "low_val": float(self.low_val),
                "close_val": float(self.close_val), "adj_close_val": float(self.adj_close_val),
                "volume": float(self.volume)}

    def __repr__(self):
        return f"StockModel(id={self.id!r}, stock_id={self.stock_id!r}, " \
               f"stock_date={self.stock_date!r}), open_val={self.open_val!r}), high_val=" \
               f"{self.high_val!r}), low_val={self.low_val!r}), close_val={self.close_val!r})," \
               f"adj_close_val={self.adj_close_val!r}), volume={self.volume!r})"

    @classmethod
    def fetch_listings_by_name(cls, name):
        stock_code = StocksCodeModel.find_by_name(name)
        if stock_code is not None:
            return cls.query.filter(StockModel.stock_id == stock_code.id)\
                .order_by(StockModel.stock_date)

    def save_to_db(self):
        try:
            db_session.add(self)
            db_session.commit()
        except (SQLAlchemyError, DBAPIError) as error:
            db_session.rollback()
            raise DataError(statement=error.statement, params=error.params,
                            orig=error.orig, code=error.code)

    @classmethod
    def delete_from_db(cls, stock_code):
        if stock_code is not None:
            stmt = delete(cls).where(cls.stock_id == stock_code.id)
            db_session.execute(stmt)
            db_session.commit()


