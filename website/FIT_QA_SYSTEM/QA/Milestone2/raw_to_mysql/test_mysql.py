import pymysql.cursors
from getCategories import getCategory


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Dg1AvHjj',
                             db='FIT_QA_System',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def add_Category(category):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `IT_Category` (`category_name`) VALUES (%s)"
            for c in category:
                cursor.execute(sql, c)
                print(c)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":
    category = getCategory()
    print(category)
    add_Category(category)
