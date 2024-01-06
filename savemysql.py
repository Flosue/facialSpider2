import pymysql

def save(num,pic1):
    conn = pymysql.connect(host='localhost', port=3306, user='wty', password='123456', db='network', charset='utf8')
    cursor = conn.cursor()

    try:
     # 执行sql语句
        cursor.execute( "insert into relation(mainname,point,pic) values (%s,%s,%s)",(r'e:/project/1_1.jpg',num,pic1))
     # 提交到数据库执行
        conn.commit()
        print(1)
    except Exception as e:
     # 如果发生错误则回滚
        print(e)
        conn.rollback()
        print(2)

    cursor.close()

    conn.close()
