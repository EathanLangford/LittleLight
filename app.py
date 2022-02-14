from distutils.command.clean import clean
from inspect import currentframe
import requests
import urllib.request
import time
import json
from bs4 import BeautifulSoup
import re

headers = {'Host':'www.metacritic.com',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'Accept-Language':'en-US,en;q=0.5',
'Accept-Encoding':'gzip, deflate, br',
'Connection':'keep-alive',
'Cookie':'OptanonConsent=isIABGlobal=false&datestamp=Wed+Feb+09+2022+01%3A25%3A28+GMT%2B1100+(Australian+Eastern+Daylight+Time)&version=6.20.0&hosts=&consentId=5e6fb341-b25b-4c68-8300-8d0807bc503a&interactionCount=0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=AU%3BVIC; mc_s_s=a_2; _BB.bs=b|1; utag_main=v_id:017ed356ceec0004b903c8abae490004e004c00d00bd0$_sn:5$_ss:1$_st:1644332130106$vapi_domain:metacritic.com$_pn:1%3Bexp-session$ses_id:1644330329505%3Bexp-session; prevPageType=article; AMCV_3C66570E5FE1A4AB0A495FFC%40AdobeOrg=1585540135%7CMCIDTS%7C19031%7CMCMID%7C20043071234403274291640894182928763551%7CMCAAMLH-1644935129%7C8%7CMCAAMB-1644935129%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1644337530s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19038%7CvVersion%7C4.4.0; AMCVS_3C66570E5FE1A4AB0A495FFC%40AdobeOrg=1; chsn_cnsnt=tglr_ref%2Ctglr_req%2Ctglr_sess_id%2Ctglr_sess_count%2Ctglr_anon_id%2Ctglr_tenant_id%2Ctglr_virtual_ref%2Ctglr_transit_id%2Cchsn_dcsn_cache%2Cpmpdid%2Cpmpredirected%2Cpmpredir%2Cfuseid%2Ccohsn_xs_id%2Cchsn_auth_id%2ChashID%2CetagID%2CreinforcedID%2ChttpOnlyID%2CfpID%2CflID%2Ctglr_smpl%2Ctglr_reinforce%2Ctglr_gpc_sess_id%2Ctglr_hash_id; tglr_tenant_id=src_1kZD6ZLXVCIj0d2XTZb7WONLbaA; tglr_sess_count=5; tglr_anon_id=e80a74c8-3c2d-4570-bcd7-258f2a5f0ff6; s_ecid=MCMID%7C20043071234403274291640894182928763551; ctk=NjIwMGRhZDQ3OWM4MTcwNDk0MzY5ODQ1NTMzNg%3D%3D; cohsn_xs_id=d1c0fee9-fc88-472d-b565-5bd79cbfab00; s_cc=true; aam_uuid=12395272332450396452028508067124288903; RT="z=1&dm=metacritic.com&si=f70a1d38-97aa-4d0d-b8bc-6125f77bb290&ss=kze7tiqd&sl=0&tt=0&bcn=%2F%2F684d0d49.akstat.io%2F&ld=3hqyo&ul=12cn"; _cb_ls=1; _cb=BKodM_CXMRlZBfyB3x; _chartbeat2=.1640427506602.1644330329043.0000000000000111.D5O-baCnWjTF1DKS5BGScZFCF5LQ6.1; __utma=15671338.2062571073.1644223190.1644324472.1644330332.5; __utmc=15671338; __utmz=15671338.1644324472.4.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); OptanonAlertBoxClosed=2022-02-08T14:25:28.579Z; metapv=3; _BB.d=0|||3; _BB.enr=0; _cb_svref=null; tglr_sess_id=8de68a19-05d8-4686-aa35-4f3506dc1df3; tglr_req=https://www.metacritic.com/feature/new-free-games-playstation-xbox-pc-switch; tglr_ref=; __utmb=15671338.1.10.1644330332; __utmt=1',
'Upgrade-Insecure-Requests':'1',
'Sec-Fetch-Dest':'document',
'Sec-Fetch-Mode':'navigate',
'Sec-Fetch-Site':'none',
'Sec-Fetch-User':'?1',
'Cache-Control':'max-age=0',
'TE':'trailers'}
url = 'https://www.metacritic.com/feature/new-free-games-playstation-xbox-pc-switch'

response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, “html.parser”)
soup = BeautifulSoup(response.text, "html.parser")
# soup = BeautifulSoup(response.text, "html.parser").encode("utf-8")
allTables = soup.findAll('table', class_='linedtable')
allTableTitles = soup.findAll('h2', class_='captionstyle')

# find all tds

# print(testTds[0])
jsonArray = []
# loop through each table, get each tr, every second is useless.

for i in range(len(allTableTitles)):
    allGamesOneTable = []
    trsInTable = allTables[i].findAll('tr')
    del trsInTable[0]


    for x in range(len(trsInTable)):

        if (trsInTable[x].get("class") == 'unlined'):
            print("--------------------NOT UNLINED BELOW--------------------")
            print(trsInTable[x])

        if (trsInTable[x].get("class") == None):
            title = trsInTable[x].find("td", {"class": "title"}).a.text if trsInTable[x].find("td", {"class": "title"}).a else trsInTable[x].find("td", {"class": "title"}).text
            date =  trsInTable[x].findAll("td", {"rowspan": 2})[1]
            where = allTableTitles[i].text
            if (date.a):
                where = date.a.text.split("\r\n                    ")
                date.a.decompose()

            # print(trsInTable[x].findAll("td", {"rowspan": 2})[1].text)

            singleGame={
                "title":title,
                # "date":trsInTable[x].findAll("td", {"rowspan": 2})[1].text.split("\u2013"),
                "date":trsInTable[x].findAll("td", {"rowspan": 2})[1].text.replace("\r","").replace("\n                    ","").split("\u2013"),
                # "date":trsInTable[x].findAll("td", {"rowspan": 2})[1].text,
                "where": where
            }
            allGamesOneTable.append(singleGame)

    singleTable = {
        "title": allTableTitles[i].text,
        "games": allGamesOneTable
    }
    jsonArray.append(singleTable)

# now i need to go through, get only: Free for Everyone, PSPlus, PC Game Pass, Xbox Game Pass(maybe?)
# template message 
# Game title
# Date
# Table Title (where to get the game)
# eg:
# 
# 
# Yooka-Laylee and the Impossible Lair
# February 3
# Epic Game Store
# 
#       {
#         "title": "Yooka-Laylee and the Impossible Lair",
#         "date": [
#           "February 3",
#           "February 9"
#         ]
#       }
print(json.dumps(jsonArray, indent=2))