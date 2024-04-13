from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class get_data(db.Model):
    __tablename__ = 'DB_table'
    id = Column(Integer, primary_key=True)
    價格 = Column(String(255))  # 或者您也可以使用 Text 类型
    名稱 = Column(String(255))  # 或者您也可以使用 Text 类型
    地址 = Column(String(255))  # 或者您也可以使用 Text 类型
    坪數 = Column(String(255))  # 或者您也可以使用 Text 类型
    屋齡 = Column(String(255))  # 或者您也可以使用 Text 类型
    樓層 = Column(String(255))  # 或者您也可以使用 Text 类型
    車位 = Column(String(255))  # 或者您也可以使用 Text 类型
    來源 = Column(String(255))  # 或者您也可以使用 Text 类型
    類型 = Column(String(255))  # 或者您也可以使用 Text 类型
    起始租金_首付款 = Column(Integer)
    每月繳金額 = Column(Integer)
