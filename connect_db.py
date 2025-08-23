import pymysql

def Connect():
    #Funcion para conectarse
    return pymysql.connect(
        host="",
        user="root",
        password="",
        database="",
        cursorclass = pymysql.cursors.DictCursor
    )


