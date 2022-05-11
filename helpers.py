from ast import parse
import asyncio
from distutils.command.clean import clean
from inspect import currentframe
from time import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import re
import json
import platform
if platform.system() == 'Windows':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# bot.py
from dotenv import load_dotenv
import os






def getRaw():
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
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def cleanseDate(date):
    parseDate = date.text
    parseDate = parseDate.replace("PlayStation Store", "")
    parseDate = parseDate.replace("Epic Games Store", "")
    parseDate = parseDate.replace("IndieGala", "")
    parseDate = parseDate.replace("Microsoft", "")
    parseDate = parseDate.replace("Steam",  '')
    parseDate = parseDate.replace("Itch.io",  '')
    parseDate = parseDate.replace("\r","")
    parseDate = parseDate.replace("\n                    ","")
    parseDate = parseDate.replace("Store","")
    return ' '.join(parseDate.split('–')[0].split())

def dateAsDateTime(tagDate):
    dateTime = datetime.strptime(tagDate,r"%B %d")
    dateTime = dateTime.strftime(r"%B %d")
    return dateTime

def getData(soup):
    scrapedData = []
    #GET ALL HTML TABLES THAT POINT TO THE DATA WE WANT
    allTables = soup.findAll('table', class_='linedtable')
    allTableTitles = soup.findAll('h2', class_='captionstyle')

    #LOOP THROUGH EACH TABLE
    for i in range(len(allTableTitles)):
        gamesInSingleTable = []
        trsInTable = allTables[i].findAll('tr')
        #DELETE WHITE SPACE AT START OF TABLES
        del trsInTable[0]

        #LOOP THROUGH HTML TABLE
        for x in range(len(trsInTable)):

            if (trsInTable[x].get("class") == 'unlined'):
                print(trsInTable[x])

            #GAMES ARE REPRESENTED AS CLASS NONE
            if (trsInTable[x].get("class") == None):
                #GAME EXTRACT
                title = trsInTable[x].find("td", {"class": "title"}).a.text if trsInTable[x].find("td", {"class": "title"}).a else trsInTable[x].find("td", {"class": "title"}).text
                date =  trsInTable[x].findAll("td", {"rowspan": 2})[1]
                where = allTableTitles[i].text.replace("($) ","")

                parseDate = cleanseDate(date)

                #PLAYSTATION STORE BUG
                if "[" in where:
                    where = where.split("[")[0]
               
                if (date.a):
                    where = date.a.get("href")
                    for br in date.findAll('br'):
                        br.extract()
                    for a in date.findAll('a'):
                        a.extract()

                singleGame={
                    "title":title,
                    "date": dateAsDateTime(parseDate),
                    "where": where
                }
                gamesInSingleTable.append(singleGame)

        singleTable = {
            "title": allTableTitles[i].text,
            "games": gamesInSingleTable,
            "sort": where
        }
        scrapedData.append(singleTable)
    return scrapedData

#REMOVE DUPLICATES FROM PARSE BUG
def removeDuplicates(data):
    seen = {}
    for platform in data:
        for obj in platform["games"]:
            if obj["title"] in seen.keys():
                platform["games"].remove(obj)
            else:
                seen[obj["title"]] = 1
    return data    

#SUBTRACT DAYS FROM TIMESTAMP TO RUN FOR PREVIOUS DAYS IF NEED
def subractDays(currentTime, days):
        subtractDays = timedelta(days)
        currentTime = currentTime - subtractDays
        currentTime = currentTime.strftime(r"%B %d")
        print(currentTime)
        return currentTime

#GET CHANNEL FOR SEND MESSAGE
def getChannel(game, client):
        #TODO swap ENV calls for SSM calls
        general_channel_id = int(os.getenv('general_channel_id'))
        playstationPlus_channel_id = int(os.getenv('playstationPlus_channel_id'))
        free_channel_id = int(os.getenv('free_channel_id'))
        humble_channel_id = int(os.getenv('humble_channel_id'))
        playstationNow_channel_id = int(os.getenv('playstationNow_channel_id'))
        prime_channel_id = int(os.getenv('prime_channel_id'))
        stadia_channel_id = int(os.getenv('stadia_channel_id'))
        xboxGold_channel_id = int(os.getenv('xboxGold_channel_id'))
        xboxGamePass_channel_id = int(os.getenv('xboxGamePass_channel_id'))
        pcGamepass_channel_id = int(os.getenv('pcGamepass_channel_id'))
        
        #TODO fix repitition
        if ("Free for everyone" in game):
            return client.get_channel(free_channel_id)
        if ("Humble Choice" in game["where"]):
            return client.get_channel(humble_channel_id)
        if ("PC Game Pass" in game["where"]):
            return client.get_channel(pcGamepass_channel_id)
        if ("PlayStation Now" in game["where"]):
            return client.get_channel(playstationNow_channel_id)    
        if ("PlayStation Plus" in game["where"]):
            return client.get_channel(playstationPlus_channel_id)
        if ("Prime Gaming" in game["where"]):
            return client.get_channel(prime_channel_id)
        if ("Stadia" in game["where"]):
            return client.get_channel(stadia_channel_id)
        if ("Xbox Games" in game["where"]):
            return client.get_channel(xboxGold_channel_id)
        if ("Xbox Game Pass" in game["where"]):
            return client.get_channel(xboxGamePass_channel_id)


async def postToChannels(client, jsonArray):
#TODO its picking up XBOX in XBOX GamePass and others because its not doing an exact match, its matching to multiple ifs
        urlWorkaround = ""
        timestamp = datetime.now()
        timestamp = subractDays(timestamp, 1)

        for table in range(len(jsonArray)):
            for game in range(len(jsonArray[table]["games"])):
                currentGame = jsonArray[table]["games"][game]
                currentPlatform = jsonArray[table]["sort"]

                #CHECK CURRENT TIME AGAINST RELEASE DATE
                if (currentGame["date"] == timestamp):
                    if ("Free for everyone" in currentGame):
                        urlWorkaround = currentGame["where"]
                    channel = getChannel(currentGame, client)
                    
                    #SEND TO CHANNEL
                    await channel.send(">>> ***"+jsonArray[table]["games"][game]["title"] +"*** "+jsonArray[table]["games"][game]["date"] +urlWorkaround)
                    
                    # PRINT INSTEAD OF SEND
                    # print(("\n>>> ***"+jsonArray[table]["games"][game]["title"] +" "+jsonArray[table]["games"][game]["date"] + "*** "+jank))                    
        print('🗸')               

