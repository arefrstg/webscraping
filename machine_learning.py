import mysql.connector

cnx = mysql.connector.connect(user='root', password='AaA123456789@', host='127.0.0.1')
cursor = cnx.cursor()
#
# cursor.execute("INSERT INTO web_data.category (cat_title, cat_url, maxpage_done) VALUES (\'%s\', \'%s\', \'%s\');)" % (
#     "title_category", "category_url", "str(max_page)"))
cursor.execute("select * from web_data.category ")
for a in cursor:
    print(a)

cnx.commit()
cursor.close()
