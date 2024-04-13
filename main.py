from flask import Flask, render_template, request
from mods.model import get_data as ModelUser  # 匯入資料模型
from mods.model import db  # 匯入資料庫實例
from sqlalchemy import and_, or_, func  # 匯入 SQLAlchemy 的一些方法

app = Flask(__name__)  # 創建 Flask 應用
app.config["DEBUG"] = True  # 啟用偵錯模式

# 設定資料庫連線資訊
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://DB_user:DB_password@DB_IP/database'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化資料庫實例
db.init_app(app)

# 首頁路由
@app.route('/', methods=['GET'])
def index():
    # 直接調用 get_data_route() 函數獲取資料
    data = get_data_route()
    return render_template('index.html', data=data)

# 獲取資料的路由
def get_data_route():
    # 獲取請求參數的值
    price_min = request.args.get("price_min")
    price_max = request.args.get("price_max")
    has_parking = request.args.get("has_parking")
    house = request.args.get("type")

    # 如果最低價格未提供，則設置為最小值
    if price_min == "":
        price_min = db.session.query(func.min(ModelUser.每月繳金額)).scalar()

    # 如果最高價格未提供，則設置為最大值
    if price_max == "":
        price_max = db.session.query(func.max(ModelUser.每月繳金額)).scalar()
        
    filters = []  # 創建過濾條件列表

    # 根據屋型參數添加過濾條件
    if house == "type_true":
        filters.append(ModelUser.類型 == "租屋")
    elif house == "type_false":
        filters.append(ModelUser.類型 == "買屋")

    # 根據價格範圍參數添加過濾條件
    if price_min and price_max:
        filters.append(ModelUser.每月繳金額.between(price_min, price_max))

    # 根據是否有停車位參數添加過濾條件
    if has_parking == "true":
        filters.append(and_(ModelUser.車位 != "無", ModelUser.車位 != "無車位"))
    elif has_parking == "false":
        filters.append(or_(ModelUser.車位 == "無", ModelUser.車位 == "無車位"))

    # 如果沒有提供過濾條件，則返回所有資料
    if not filters:
        rows = ModelUser.query.all()
    else:
        rows = ModelUser.query.filter(*filters).all()

    # 將查詢到的資料轉換成字典列表
    user_info = [{
        "id": row.id,
        "price": row.價格,
        "name": row.名稱,
        "address": row.地址,
        "area": row.坪數,
        "age": row.屋齡,
        "floor": row.樓層,
        "parking": row.車位,
        "source": row.來源,
        "type": row.類型,
        "payment_start": row.起始租金_首付款,
        "monthly_payment": row.每月繳金額,
    } for row in rows]

    return user_info  # 直接返回資料列表

if __name__ == '__main__':
    # 啟動 Flask 應用
    app.run(host='0.0.0.0', port=80, debug=True)
