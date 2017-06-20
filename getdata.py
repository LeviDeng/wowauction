#coding:utf8
import requests
import pymongo
import time

#REGION=['us','eu','tw','kr']
TIME_SLEEP=600
REGION='us'
REALM='medivh'
LOCALE='en_US'
APIKEY='v3rwfezdh3vxj7wpwh644vugkbuemyfz'

class wowAuction():
    def __init__(self):
        self.baseUrl="https://%s.api.battle.net/wow/auction/data/"%REGION
        self.auctionUrl=self.baseUrl+"%s?locale=%s&apikey=%s"%(REALM,LOCALE,APIKEY)
        self.datetime=time.strftime("%Y%m%d%H",time.localtime())
        #print self.auctionUrl

    def getDataUrl(self):
        html=requests.get(self.auctionUrl)
        return html.json()['files'][0]['url']

    def getData(self):
        con=pymongo.MongoClient('localhost',27017)
        coll=con['wowAuction'][REGION]
        data_url=self.getDataUrl()
        res=requests.get(data_url)
        data=res.json()
        data['time'] = self.datetime
        coll.insert_one(data)
        self.itemlist=coll.distinct("auctions.item")
        con.close()

    def analyse(self):
        con=pymongo.MongoClient('localhost',27017)
        coll1=con['wowAuction'][REGION]
        coll2=con['wowAuction'][REGION+"_stat"]
        data1=coll1.find({"time":self.datetime})[0]['auctions']
        data2={"time":self.datetime}
        for i in self.itemlist:
            data2[str(i)]=[]
            for d in data1:
                if d['item']==i:
                    data2[str(i)].append(d['buyout'])
            data2[str(i)]=sorted(data2[str(i)])
        coll2.insert_one(data2)

if __name__=='__main__':
    wa=wowAuction()
    wa.getData()
    wa.analyse()