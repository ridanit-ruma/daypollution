import pymysql

database = pymysql.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'mangi0607db!',
    database = 'daypollution',
    charset = 'utf8'
)
