import json
import pymysql
import datetime

with open("api\\src\\config.json", 'r') as openfile:
    user = json.load(openfile)['user']
    password = json.load(openfile)['password']
    database = json.load(openfile)['database']

database = pymysql.connect(
    host = '127.0.0.1',
    user = user,
    password = password,
    database = database,
    charset = 'utf8'
)

def addData(data:list):
    print(data)
    cursor = database.cursor()
    for i in range(len(data)):
        onedata = data[i]
        timedata = onedata['tm'].split('-')
        y = int(timedata[0])
        m = int(timedata[1])
        d = int(timedata[2])
        datas = [datetime.datetime(y, m, d).date()]
        if onedata['avgTa'] == '':
            datas.append(404)
        else:
            datas.append(onedata['avgTa'])
        sql = "INSERT INTO temp (date, avgtemp) VALUE (%s, %s)"
        cursor.execute(sql, datas)
    
    database.commit()
    cursor.close()

def getData(startdate: datetime, enddate: datetime = None):
    cursor = database.cursor()
    if enddate == None:
        sql = "SELECT * FROM temp WHERE date = %s"
        cursor.execute(sql, startdate)
    else:
        sql = "SELECT * FROM temp WHERE date >= %s AND date <= %s"
        cursor.execute(sql, (startdate, enddate))
    fetchresult = cursor.fetchall()
    result = []
    for i in range(len(fetchresult)):
        result.append([str(fetchresult[i][0]), fetchresult[i][1]])
    cursor.close()
    return result
