
from sqlalchemy import Column, Boolean, String, Float, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class GStk(Base):

    __tablename__ = 'gstk'

    search_id   = Column(String(180), primary_key=True)
    exchange    = Column(String(180), nullable=False)
    code        = Column(String(180), nullable=False, unique=True)
    tradable    = Column(Boolean(), default=False)

    def to_dict(self):
        return { 'search_id': self.search_id, 'exchange': self.exchange, 'code': self.code, 'tradable': self.tradable }


class GStkDayStat(Base):
    
    __tablename__ = 'gstk_day_stat'

    search_id       = Column(String(180), primary_key=True)
    open_price      = Column(Float(precision=2), default=0.00)
    live_price      = Column(Float(precision=2), default=0.00)
    day_change      = Column(Float(precision=3), default=0.00)
    day_change_perc = Column(Float(precision=3), default=0.00)



