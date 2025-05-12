import pymysql

from database import db_config # 从database.py中导入数据库配置
LOWBP = (130+80)/2
HIGHBP = (140+90)/2

# 下面的代码中使用lipids代表血脂，使用Bg代表血糖，使用Bp代表血压

'''
在 Python 的 pymysql 库中，pymysql.cursors.DictCursor 是一个用于将查询
结果返回为字典格式的游标类型。通常，使用 pymysql 进行数据库查询时，默认情
况下查询结果返回为元组。使用 DictCursor 可以方便地将每一行数据转换为字典，
其中列名作为字典的键，列的值作为字典的值

'''

def judgeLipids(value: float) -> str:
    if value > 0 and value < 3:
        return '10'
    elif value >= 3 and value < 5.7:
        return '01'
    elif value >= 5.7:
        return '00'
    raise ValueError("血脂值应该为正数")


def judgeBg(value: float) -> str:
    if value > 0 and value < 6:
        return '10'
    elif value >= 6 and value < 10:
        return '01'
    elif value >= 10:
        return '00'
    raise ValueError("血糖值应该为正数")


def judgeBp(value: float) -> str:
    if value > 0 and value < LOWBP:
        return '10'
    elif value >= LOWBP and value < HIGHBP:
        return '01'
    elif value >= HIGHBP:
        return '00'
    raise ValueError("血压值应该为正数")


def concatenate_high(a: str, b: str) -> str:
    """
    将整数 a 的二进制表示连接到整数 b 的高位。
    参数：
    a (int): 要放置在高位的整数。
    b (int): 要放置在低位的整数。
    返回:int: 连接后的结果整数。
    """
    # # Calculate the number of bits in b
    # num_bits_b = b.bit_length()
    # # Left shift a by the number of bits in b
    # a_shifted = a << num_bits_b
    # # Combine a_shifted and b using bitwise OR
    # combined = a_shifted | b
    return a+b


def concat(lipids, bg, bp):

    try:

        lipidCode = judgeLipids(lipids)
        bgCode = judgeBg(bg)
        bpCode = judgeBp(bp)

        health_lipid = concatenate_high('00', lipidCode)
        health_bg = concatenate_high('01', bgCode)
        health_bp = concatenate_high('10', bpCode)
    except ValueError as e:
        print(e)
        # TODO 这里可以修改返回一个负数，再在下面的代码中加上一个循环，让用户可以重复输入
        exit(1)
    return health_lipid, health_bg, health_bp


def getResults(sql: str):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
        '''
        results是一个类似于下面这样的数据结构(因为在数据库配置中指定了游标类型为DictCursor)：
        [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}, {'id': 3, 'name': 'Charlie'}]
        '''
        return results


def find_matching_substrings(long_binary_str, short_binary_list) -> bool:
    # 遍历短的二进制串数组
    for short_binary_str in short_binary_list:
        # 判断该短二进制串是否是长二进制串的一部分
        if short_binary_str in long_binary_str:
            return True


def getFoodList(results):
    food_list = list()
    total = concatenate_high(health_bg, health_bp)
    total = concatenate_high(health_lipid, total)
    for row in results:
        # row['food_code'] 应该为以逗号分隔的特征码，只要食物具有某个特征码，则代表食物适合某一类人吃
        food_code = str(row['food_code'])
        codes = food_code.split(',')
        if find_matching_substrings(total, codes):
            food_list.append(row['food_name'])
    return food_list


if __name__ == "__main__":

    height = float(input("输入你的身高(m)："))
    weight = float(input("输入你的体重(kg)："))
    lipids = float(input("输入你的血脂浓度(mmol/L)："))
    bg = float(input("输入你的血糖浓度(mmol/L)："))
    sbp = float(input("输入你的收缩血压(mmHg)："))
    dbp = float(input("输入你的舒张血压(mmHg)："))
    bp = (sbp+dbp)/2
    bmi = weight/(height**2)

    if bmi < 18.5:
        health_lipid, health_bg, health_bp = concat(lipids, bg, bp)
    elif bmi >= 18.5 and bmi < 24:
        initCode = '11'
        health_lipid, health_bg, health_bp = concat(lipids, bg, bp)
        health_lipid = concatenate_high(initCode, health_lipid)
        health_bg = concatenate_high(initCode, health_bg)
        health_bp = concatenate_high(initCode, health_bp)
    elif bmi >= 24:
        initCode = '1111'
        health_lipid, health_bg, health_bp = concat(lipids, bg, bp)
        health_lipid = concatenate_high(initCode, health_lipid)
        health_bg = concatenate_high(initCode, health_bg)
        health_bp = concatenate_high(initCode, health_bp)

    # 连接数据库
    connection = pymysql.connect(**db_config)

    while True:
        mealtype = input("你想吃早餐？午餐？晚餐？请输入：")
        if mealtype == '早餐':
            sql = "select * from health.breakfast"
            results = getResults(sql)
            food_list = getFoodList(results)
            break
        elif mealtype == '午餐':
            sql = "select * from health.lunch"
            results = getResults(sql)
            food_list = getFoodList(results)
            break
        elif mealtype == '晚餐':
            sql = "select * from health.dinner"
            results = getResults(sql)
            food_list = getFoodList(results)
            break
        else:
            print("输入不合法，请重新输入")

    for item in food_list:
        print(item)
