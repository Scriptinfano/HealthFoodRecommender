"""
这个脚本用于删除并重新创建 health 库
"""
import pymysql
from database import db_config as base_config
# 连接配置（不指定 database，先连接到 MySQL）


# 要创建的数据库名
db_name = "health"

# DDL 和数据插入语句
ddl_sql = f"""
CREATE DATABASE IF NOT EXISTS {db_name};
USE {db_name};

CREATE TABLE IF NOT EXISTS breakfast (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    food_name VARCHAR(255) NOT NULL,
    food_code VARCHAR(8) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS lunch (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    food_name VARCHAR(255) NOT NULL,
    food_code VARCHAR(8) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS dinner (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    food_name VARCHAR(255) NOT NULL,
    food_code VARCHAR(8) NOT NULL,
    description TEXT
);

ALTER TABLE breakfast AUTO_INCREMENT = 1;
ALTER TABLE lunch AUTO_INCREMENT = 1;
ALTER TABLE dinner AUTO_INCREMENT = 1;

INSERT INTO breakfast (food_name, food_code, description) VALUES
    ('Scrambled Eggs', '10101101', 'Delicious scrambled eggs with toast.'),
    ('Oatmeal', '1100', 'Healthy oatmeal with fruits and nuts.'),
    ('Smoothie', '1001', 'Refreshing fruit smoothie.'),
    ('Pancakes', '1011', 'Fluffy pancakes with maple syrup.'),
    ('Yogurt', '1000', 'Creamy yogurt with granola and berries.');

INSERT INTO lunch (food_name, food_code, description) VALUES
    ('Grilled Chicken Salad', '1010', 'Grilled chicken breast with mixed greens.'),
    ('Vegetable Stir-fry', '1110', 'Colorful stir-fried vegetables with tofu.'),
    ('Quinoa Salad', '1100', 'Nutritious quinoa salad with avocado.'),
    ('Sandwich', '1001', 'Classic sandwich with ham, cheese, and veggies.'),
    ('Soup', '1011', 'Homemade soup with fresh ingredients.');

INSERT INTO dinner (food_name, food_code, description) VALUES
    ('Salmon with Asparagus', '1010', 'Baked salmon fillet served with asparagus.'),
    ('Pasta with Marinara Sauce', '1100', 'Pasta tossed in tangy marinara sauce.'),
    ('Steak with Potatoes', '1110', 'Grilled steak served with roasted potatoes.'),
    ('Vegetarian Curry', '1001', 'Flavorful vegetarian curry with rice.'),
    ('Sushi', '1011', 'Assorted sushi rolls with soy sauce and wasabi.');
"""

# 拆分语句并逐条执行
statements = [stmt.strip()
              for stmt in ddl_sql.strip().split(';') if stmt.strip()]

connection = None  # 提前定义

try:
    connection = pymysql.connect(**base_config)
    with connection.cursor() as cursor:
        # 删除数据库
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
        print(f"✅ 数据库 {db_name} 已删除！")
        print("即将重新创建数据库...")
        # 创建数据库并使用
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        cursor.execute(f"USE {db_name};")

        # 执行表创建和数据插入语句
        for stmt in statements:
            cursor.execute(stmt)
        connection.commit()
        print(f"✅ 数据库 {db_name} 及所有表和数据创建成功！")

except Exception as e:
    print("❌ 出错了：", e)

finally:
    if connection:  # 只有在连接成功的情况下才关闭
        connection.close()

