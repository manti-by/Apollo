from sqlalchemy import Column, Integer, Float, SmallInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Record(Base):
    __tablename__ = 'record'

    id = Column(Integer, primary_key = True)
    
    term_01 = Column(Float, default = 0.0)
    term_02 = Column(Float, default = 0.0)
    term_03 = Column(Float, default = 0.0)
    term_04 = Column(Float, default = 0.0)
    term_05 = Column(Float, default = 0.0)
    
    water_sensor = Column(SmallInteger, default = 0)
    
    timestamp = Column(DateTime)

    def __repr__(self):
        return '<Record #%d>' % (self.id)
