from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Time, ForeignKey, DateTime

Base = declarative_base()


class VideoClass(Base):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), default=None, comment="文件名")
    time = Column(DateTime, comment="检测时间")
    helmet = Column(Integer, default=0, nullable=False, comment="佩戴安全帽总人数")
    head = Column(Integer, default=0, nullable=False, comment="未佩戴安全帽总人数")
    total = Column(Integer, default=0, nullable=False, comment="总人数")


class DataClass(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    vid = Column(Integer, ForeignKey("result.id", ondelete='CASCADE'))
    time = Column(Time, comment="帧时间")
    helmet = Column(Integer, default=0, nullable=False, comment="佩戴安全帽总人数")
    head = Column(Integer, default=0, nullable=False, comment="未佩戴安全帽总人数")
    total = Column(Integer, default=0, nullable=False, comment="总人数")
