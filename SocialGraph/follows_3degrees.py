import logging
import asyncio
from nostr.key import PublicKey
from monstr.client.client import Client, ClientPool
from monstr.client.event_handlers import PrintEventHandler
from monstr.event.event import Event
from monstr.encrypt import Keys
import psycopg2 #librería para conectar al Postgresql
import pandas as pd
import requests
from datetime import datetime
import time
#export PYTHONPATH="$PYTHONPATH:./"

def ConnectingToDB(DBParams):
    return(psycopg2.connect(database=DBParams['database'], user=DBParams['user'], password=DBParams['password'],host=DBParams['host'], port= DBParams['port']))

DBParams = {'database':'postgres', 'user':'postgres', 'password':'postgres', 'host':'localhost', 'port':'5432'}


#calling few relays 
DEFAULT_RELAY=["wss://relay.damus.io","wss://nostr.wine", "wss://offchain.pub"]

nico_follows= []


#connecting to the database and storing all Nico's follows
#this function will query all event's kind 3 from Nico's PubKey in a set of relays
#event's kind 3 are the ones where we share our contact list
async def one_off_query_by_pub(relay=DEFAULT_RELAY):

    conn = ConnectingToDB(DBParams)
    cursor = conn.cursor()
    nico_pub = ['0000000033f569c7069cdec575ca000591a31831ebb68de20ed9fb783e3fc287']
    for r in relay:
        async with Client(r) as c:
            events = await c.query({
                'kinds':[3],
                'authors': nico_pub,
                'since':int((datetime.strptime('2023-03-01 00:00', '%Y-%m-%d %H:%M').timestamp()))
            })
            for c_evt in events:
                for x in c_evt.tags:
                    try:
                        cursor.execute("INSERT INTO public.follows_l1 (user_pub, follows_l1_pub) VALUES('{}', '{}');".format(nico_pub[0],x[1]))    
                    except:
                        pass
                conn.commit()
    conn.close()

#With Nico's followers listed, the process will now continue querying the next degree of separation
#for each follow, I'll extract their follows

async def followers_follows(relay=DEFAULT_RELAY):
    """
    doing a basic query using with to manage context
    :param relay:
    :return:
    """

    conn = ConnectingToDB(DBParams)
    cursor = conn.cursor()
    cursor.execute("SELECT follows_l1_pub FROM follows_l1")
    follows = cursor.fetchall()
    authors_list = []
    for x in follows:
        authors_list.append(x[0])
    for r in relay:
        async with Client(r) as c:
            events = await c.query({
                'kinds':[3],
                'authors': authors_list,
                'since':int((datetime.strptime('2023-03-01 00:00', '%Y-%m-%d %H:%M').timestamp()))
            })
            for c_evt in events:
                for x in c_evt.tags:
                    try:
                        cursor.execute("INSERT INTO public.follows_l2 (follows_l1_pub, follows_l2_pub) VALUES('{}', '{}');".format(c_evt.pub_key,x[1]))    
                        print(c_evt.pub_key + ' ' + x[1])
                    except:
                        print('Duplicated follow: '+ str(x[1]))
                conn.commit()
    conn.close()

#The process will repeat with the subsequent level 

async def followers_follows2(relay=DEFAULT_RELAY):
    """
    doing a basic query using with to manage context
    :param relay:
    :return:
    """

    conn = ConnectingToDB(DBParams)
    cursor = conn.cursor()
    cursor.execute("select distinct follows_l3_pub from follows_l3")
    follows = cursor.fetchall()
    authors_list = []
    for x in follows:
        authors_list.append(x[0])
    for r in relay:
        async with Client(r) as c:
            events = await c.query({
                'kinds':[3],
                'authors': authors_list[8000:],
                'since':int((datetime.strptime('2023-03-01 00:00', '%Y-%m-%d %H:%M').timestamp()))
            })
            for c_evt in events:
                for x in c_evt.tags:
                    try:
                        cursor.execute("INSERT INTO public.follows_l3 (follows_l2_pub, follows_l3_pub) VALUES('{}', '{}');".format(c_evt.pub_key,x[1]))    
                        print(c_evt.pub_key + ' ' + x[1])
                    except:
                        print('Duplicated follow: '+ str(x[1]))
                conn.commit()
    conn.close()



async def main():
    await one_off_query_by_pub()
    await followers_follows()
    await followers_follows2()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    asyncio.run(main())



conn = ConnectingToDB(DBParams)
cursor = conn.cursor()
# Since there will be repeated pubkeys, we'll now create a new table with only distinct 3rd degree pubkeys

cursor.execute("SELECT DISTINCT follows_l3_pub FROM follows_l3")
follows_plus = cursor.fetchall()
nico_pub = ['0000000033f569c7069cdec575ca000591a31831ebb68de20ed9fb783e3fc287']

for x in follows_plus:
    try:
        print(PublicKey(bytes.fromhex(x[0])).bech32())
        cursor.execute("INSERT INTO public.follows_plus (user_pub, follows_pub, follows_plus_bech32) VALUES('{}', '{}', '{}');".format(nico_pub[0], x[0], PublicKey(bytes.fromhex(x[0])).bech32()))
    except:
        print('Duplicated FollowsPlus:' + str(PublicKey(bytes.fromhex(x[0])).bech32()))
conn.commit()
conn.close()

