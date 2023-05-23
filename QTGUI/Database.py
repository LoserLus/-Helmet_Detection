import datetime  # 依赖
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from QTGUI.ORMClass import VideoClass, DataClass


class Database:
    def __init__(self, echo=False):
        self.engine = create_engine(
            "mysql+pymysql://{}:{}@{}:{}/{}".format('root', '123456', 'localhost', '3306', 'detection'), echo=echo)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def insert(self, name, helmet, head):
        data_time = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")  # 系统时间
        # DataFrame写入MySQL
        # 新建DataFrame
        df_write = pd.DataFrame(
            {'name': [name], 'time': [data_time],
             'helmet': [helmet], 'head': [head], 'total': [head + helmet]})
        # 将df储存为MySQL中的表，不储存index列
        df_write.to_sql('result', self.engine, index=False, if_exists='append')
        return True

    def insertData(self, datalist):
        self.session.add_all(datalist)
        self.session.commit()

    def insertResult(self, result):
        self.session.add(result)
        self.session.flush()
        self.session.commit()
        return result.id

    def queryAllResult(self):
        return self.session.query(VideoClass).all()

    def queryResultByIds(self, ids):
        return self.session.query(VideoClass).filter(VideoClass.id.in_(ids)).statement

    def queryDataById(self, vid):
        return self.session.query(DataClass).filter(DataClass.vid == vid).statement

    def updateResultCount(self, result):
        self.session.query(VideoClass).filter(VideoClass.id == result.id).update(
            {"helmet": result.helmet, "head": result.head, "total": result.total})
        self.session.commit()

    def query2Excel(self, fileName):
        sql_query = 'select * from result;'
        # 使用pandas的read_sql_query函数执行SQL语句，并存入DataFrame
        df_read = pd.read_sql_query(sql_query, self.engine)
        df_read.to_excel('./data/' + fileName + '.xlsx', index=False)
        return True
