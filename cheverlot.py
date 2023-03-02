import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
class VinSpider(scrapy.Spider):
    name='Chevrolet'
    
    def start_requests(self):
        vins=pd.read_csv(r'chev vins.csv')
        for vin in vins['vin']:
            yield scrapy.Request(f'https://www.chevrolet.com/ownercenter/api/{vin}/gfas?cb=16777551996700.4782935067564471')
    def parse(self, response, **kwargs):
        # print(response)
        data=response.json()
        for gfas in data['data']['gfas']:
#             ● Open Recalls (yes/no)
# ● Recall status (i.e., incomplete, completed, or terminated)
# ● Name of Recall
# ● Campaign/NHTSA #
# ● Date of recall announcement
# ● Brief description of the recall
# ● Safety Risk
# ● Remedy
# ● Recall status (i.e., incomplete, completed, or terminated)
            # print(gfas)
            try:
                NHTSA=gfas['governmentAgencies'][0]['govtAgencyNum']
            except:
                NHTSA=''

            try:
                description=gfas['gfaTexts'][0]['description']
                # print(gfaTexts=gfas['gfaTexts'])
            except:
                description=''

            try:
                remedy=gfas['gfaTexts'][0]['remedy']
                # print(gfaTexts=gfas['gfaTexts'])
            except:
                remedy=''

            try:
                safetyRisk=gfas['gfaTexts'][0]['safetyRisk']
                # print(gfaTexts=gfas['gfaTexts'])
            except:
                safetyRisk=''
            # print(gfaTexts)
            yield{
                # 'Open Recalls':gfas['data']['vin'],
                'Recall status':gfas['vinStatusInfo']['vinStatus'],
                'Name of Recall':gfas['title'],
                'Campaign/NHTSA':NHTSA,
                'Date of recall':gfas['vinStatusInfo']['releaseDate'],
                'description':description,
                'Safety Risk':safetyRisk,
                'Remedy':remedy,
                'link':response.url,

            }


process = CrawlerProcess(settings={
    'FEED_URI':'Chevrolet.csv',
    'FEED_FORMAT':'csv',

})

process.crawl(VinSpider)
process.start()