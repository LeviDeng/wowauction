#coding:utf8
import requests
import pymongo

#REGION=['us','eu','tw','kr']
REGION='us'
REALM='medivh'
LOCALE='en_US'
APIKEY='v3rwfezdh3vxj7wpwh644vugkbuemyfz'

class wowAuction():
    def __init__(self):
        self.baseUrl="https://%s.api.battle.net/wow/auction/data/"%REGION
        self.auctionUrl=self.baseUrl+"%s?locale=%s&apikey=%s"%(REALM,LOCALE,APIKEY)
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
        coll.update_one({"realms.name":REALM},{"$set":data},upsert=True)
        #coll.update(data,upsert=True)
        con.close()

if __name__=='__main__':
    wa=wowAuction()
    wa.getData()
