
from bs4 import BeautifulSoup
import lxml
import requests
import redis
import json

pool = redis.ConnectionPool(host='192.168.1.9')   #实现一个连接池
myRedis = redis.Redis(connection_pool=pool)
listLotteryTicket = []


def GetHistoryLotteryTicket():
    url = "http://datachart.500.com/ssq/history/newinc/history.php?start=03001&end=19052"
    wb_Data = requests.get(url)
    soup = BeautifulSoup(wb_Data.text,'xml')
    xml = soup.find_all('tr',class_='t_tr1')
    tmpListLotteryTicket = []
    for item in xml:
        tmpList = []
        for it in item.contents:
            try:
                tmpList.append(it.contents[0])
            except:
                tmpList.append('')
        tmpListLotteryTicket.append(tmpList)

    for item in tmpListLotteryTicket:
        data = {
        'thisIndex' : item[0],
        'num' : item[1],
        'red1' : item[2],
        'red2' : item[3],
        'red3' : item[4],
        'red4' : item[5],
        'red5' : item[6],
        'red6' : item[7],
        'blue1': item[8],
        'blue2': item[9],
        'allMoney' : item[10],
        'theFirstCount':item[11],
        'theFirestMoney':item[12],
        'theSecondCount':item[13],
        'theSecondMoney':item[14],
        'allPushMoney':item[15],
        'openDateTime':item[16]
        }
        listLotteryTicket.append(data)
    myRedis.set('listLotteryTicket',json.dumps(listLotteryTicket))

redisListLotteryTicket = myRedis.get('listLotteryTicket')

if(redisListLotteryTicket == None):
    GetHistoryLotteryTicket()
else:
    listLotteryTicket = json.loads(str(redisListLotteryTicket, encoding = "utf8"))

redBallCount = {}
for i in range(1,34):
    redBallCount[str(i)] = 0

buleBallCount={}
for i in range(1,17):
    buleBallCount[str(i)] = 0

for item in listLotteryTicket:
    for i in range(1,7):
        red = int(item['red'+str(i)])
        redBallCount[str(red)] = redBallCount[str(red)]+1
    blue = int(item['blue1'])
    buleBallCount[str(blue)] = buleBallCount[str(blue)] + 1

print(len(listLotteryTicket))
print(redBallCount)
print('\n')
print(buleBallCount)




