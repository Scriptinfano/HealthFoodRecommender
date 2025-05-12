from pymysql.cursors import DictCursor
# 数据库配置
db_config = {
    "user": "root",
    "password": "200329hmx",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "health",
    "charset": "utf8mb4",  # utf-8 改成 utf8mb4 更通用
    "cursorclass": DictCursor  # 注意：这里不是字符串，而是类名
}