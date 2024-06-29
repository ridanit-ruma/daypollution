#Import resources
import requests
import temp
import datetime
import json

#Variable declaration
updateDataPath = 'api\\src\\updateData.json'
lastUpdate = 19071001
apikey = ''

#Setup functions
def getDatetime(timeOrDate: bool):
    datetimenow = datetime.datetime.now()
    if timeOrDate:
        return datetimenow.time()
    else:
        return datetimenow.date()

def refreshLastUpdateDate():
    global lastUpdate
    with open(updateDataPath, 'r') as openfile:
        lastUpdate = json.load(openfile)['lastUpdateDate']

def fixLastUpdateDate(date: int):
    dataDictionary = {
        "firstDataDate":19071001,
        "lastUpdateDate":date
    }
    jsonedData = json.dumps(dataDictionary, indent=4)
    with open(updateDataPath, 'w') as outfile:
        outfile.write(jsonedData)
    
    refreshLastUpdateDate()

def updateData():
    global lastUpdate
    timenow = int(str(getDatetime(False)).replace("-", ""))
    yesturday = int(str(getDatetime(False) - datetime.timedelta(1)).replace("-", ""))
    if lastUpdate < yesturday:
        startdate = 0
        enddate = 0
        url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
        while (lastUpdate != yesturday):
            inttodate = datetime.datetime(year=int(str(lastUpdate)[0:4]), month=int(str(lastUpdate)[4:6]), day=int(str(lastUpdate)[6:8])).date()
            nextday = int(str(inttodate + datetime.timedelta(1)).replace("-", ""))
            startdate = nextday
            
            if str(startdate)[:4] == str(timenow)[:4]:
                enddate = yesturday
            else:
                enddate = int(str(startdate)[:4] + "1231")
            print(startdate, enddate)
            params = {
                'serviceKey' : apikey,
                'numOfRows' : 366,
                'pageNo' : 1,
                'dataType' : 'JSON',
                'dataCd' : 'ASOS',
                'dateCd' : 'DAY',
                'startDt' : str(startdate),
                'endDt' : str(enddate),
                'stnIds': 108
            }
            
            reqdata = {}
            while True:
                prereqdata = requests.get(url, params).text
                try:
                    prereqdata = json.loads(prereqdata)
                    if prereqdata['response']['header']['resultCode'] == '00':
                        reqdata = prereqdata
                        break
                except:
                    print("오류 ㅋ")
            temp.addData(reqdata['response']['body']['items']['item'])
            fixLastUpdateDate(enddate)
        return "We did some data update."
    else:
        return "We don't need any data update."

#Initialization
with open('api\\src\\config.json', 'r') as openfile:
    apikey = json.load(openfile)['apikey']
refreshLastUpdateDate()
updateData()

#Main functions

#temp functions
def yesturday():
    yesturday = getDatetime(False) - datetime.timedelta(1)
    result = temp.getData(yesturday)
    return result

def yearago():
    yesturday = getDatetime(False) - datetime.timedelta(1)
    if str(yesturday).split("-")[1] == "02" and str(yesturday).split("-")[2] == "29":
        return "What a rare day!"
    else:
        y = int(str(yesturday).split("-")[0]) - 1
        m = int(str(yesturday).split("-")[1])
        d = int(str(yesturday).split("-")[2])
        result = temp.getData(datetime.date(y, m, d))
        return result

def monthavg(year: int):
    

#Main codes
