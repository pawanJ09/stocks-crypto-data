from sqlalchemy import Column, Integer, String, Date, Numeric
from database import Base


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
    volume = Column(Numeric(precision=10))

    def __init__(self, *args):
        self.stock_id = args[0][0]
        self.stock_date = args[0][0]
        self.open_val = args[0][1]
        self.high_val = args[0][2]
        self.low_val = args[0][3]
        self.close_val = args[0][4]
        self.adj_close_val = args[0][5]
        self.volume = args[0][6]

    def __str__(self):
        pass

    @classmethod
    def find(cls, name):
        pass

    @classmethod
    def refresh_stocks(cls, name):
        pass
