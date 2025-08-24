import pymysql

def Connect():
    #Funcion para conectarse
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="tienda",
        cursorclass = pymysql.cursors.DictCursor
    )


