from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

Base = declarative_base()


class News(Base):
    __tablename__ = 'news'

    urod_id = Column(Integer, primary_key=True)
    link = Column(String)
    title = Column(String)
    text = Column(String)
    send_msg = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    format = Column(String)
