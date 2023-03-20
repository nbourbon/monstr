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

#export PYTHONPATH="$PYTHONPATH:./"

'''
DEFAULT_RELAY=["wss://relay.damus.io","wss://eden.nostr.land","wss://brb.io", "wss://nostr.mutinywallet.com", "wss://relay.snort.social","wss://nostr.milou.lol", "wss://puravida.nostr.land", "wss://relay.nostr.bg","wss://relay.honk.pw","wss://nostr-pub.wellorder.net","wss://nostr.mom","wss://nostr.sandwich.farm","wss://nostr.slothy.win","wss://global.relay.red","wss://relay.stoner.com","wss://nostr.einundzwanzig.space","wss://nostr.cercatrova.me","wss://nostr.swiss-enigma.ch","wss://relay.nostr-latam.link","wss://nostr.phenomenon.space","wss://nos.lol","wss://relay.current.fyi","wss://relay.nostr.band","wss://nostr-relay.derekross.me","wss://nostr.developer.li","wss://no.str.cr","wss://nostr.bongbong.com","wss://relay.sendstr.com","wss://relay.cryptocculture.com","wss://relay.nostr.scot","wss://nostr.hackerman.pro","wss://nostr.blockchaincaffe.it","wss://relay.taxi","wss://nostr.kollider.xyz","wss://nostr.massmux.com","wss://nostr.relayer.se","wss://nostr.ethtozero.fr","wss://nostr-relay.digitalmob.ro","wss://blg.nostr.sx","wss://no.str.watch","wss://nostr-relay.schnitzel.world","wss://nostr1.tunnelsats.com","wss://nostr.radixrat.com","wss://relay.t5y.ca","wss://relay.nostr.com.au","wss://knostr.neutrine.com","wss://nostr.nodeofsven.com","wss://relay.n057r.club","wss://nostrical.com","wss://nostr-relay.freedomnode.com","wss://nostr.jimc.me","wss://nostr.gromeul.eu","wss://node01.nostress.cc","wss://relay.nostr.ro","wss://relay.nostrich.de","wss://nostr.mustardnodes.com","wss://nostr-bg01.ciph.rs","wss://nostr.vulpem.com","wss://relay.ryzizub.com","wss://nostr3.actn.io","wss://nostr.bostonbtc.com","wss://nostr.bch.ninja","wss://nostr-verif.slothy.win","wss://nostr.supremestack.xyz","wss://relay.lexingtonbitcoin.org","wss://relay.nostr.moe","wss://nostr-1.nbo.angani.co","wss://nostr.zoomout.chat","wss://nostr.coollamer.com","wss://nostr.thesimplekid.com","wss://relay.nostr.express","wss://nostr.blocs.fr","wss://nostr.8e23.net","wss://nostr.rdfriedl.com","wss://nostr.shmueli.org","wss://btc.klendazu.com","wss://nostr.sabross.xyz","wss://nostr2.actn.io","wss://relay.plebstr.com","wss://nostr.uselessshit.co","wss://nostr.adpo.co","wss://relay.wellorder.net","wss://nostr.handyjunky.com","wss://relay-pub.deschooling.us","wss://nostr.satsophone.tk","wss://nostr.easydns.ca","wss://relay.dwadziesciajeden.pl","wss://nostr-relay.gkbrk.com","wss://nostr-pub1.southflorida.ninja","wss://relay.orangepill.dev","wss://nostr.600.wtf","wss://zur.nostr.sx","wss://nostr.mouton.dev","wss://e.nos.lol","wss://relay.nostr.vision","wss://nostrich.friendship.tw","wss://relay.nostrzoo.com","wss://nostream-production-5895.up.railway.app","wss://nostream.nostr.parts","wss://nostr.bitcoin.sex","wss://nostr-relay.texashedge.xyz","wss://nostr.thomascdnns.com","wss://nostr.btcmp.com","wss://relay.nostr.africa","wss://ragnar-relay.com","wss://nostr.zkid.social","wss://nostr.bitcoin-21.org","wss://nostr.com.de","wss://eosla.com","wss://nostr.data.haus","wss://relay1.gems.xyz","wss://nostrpro.xyz","wss://relay.austrich.net","wss://nostr.terminus.money","wss://nostr.0ne.day","wss://relay.valera.co","wss://nostr.sg","wss://nostr.liberty.fans","wss://nostr.cro.social","wss://nostr01.opencult.com","wss://nostr.ltbl.io","wss://nostr.reamde.dev","wss://nostr.wine","wss://nostr.koning-degraaf.nl","wss://nostr.pleb.network","wss://nostr.cheeserobot.org","wss://nostr.thank.eu","wss://relay.hamnet.io","wss://nostr.shroomslab.net","wss://relay.zhix.in","wss://nostr.primz.org","wss://nostr.truckenbucks.com","wss://nostr.rajabi.ca","wss://zee-relay.fly.dev","wss://nostr.blockpower.capital","wss://eospark.com","wss://nostr.sidnlabs.nl","wss://nostr-rs-relay.cryptoassetssubledger.com","wss://nostr.inosta.cc","wss://nostr21.com","wss://arc1.arcadelabs.co","wss://nostr.nym.life","wss://relay.nostr.distrl.net","wss://relay.zeh.app","wss://ch1.duno.com","wss://spore.ws","wss://relay.727whisky.com","wss://nostr.ch3n2k.com","wss://nostr.island.network","wss://cloudnull.land","wss://relay.nostrati.com","wss://relay-dev.cowdle.gg","wss://nostr.ginuerzh.xyz","wss://nostr.nakamotosatoshi.cf","wss://relay.1bps.io","wss://nostr1.saftup.xyz","wss://relay.nostrview.com","wss://relay.nostromo.social","wss://1.noztr.com","wss://offchain.pub","wss://nostr.nikolaj.online","wss://nostr-relay.pcdkd.fyi","wss://relay.nostr.wirednet.jp","wss://nostrsxz4lbwe-nostr.functions.fnc.fr-par.scw.cloud","wss://www.131.me","wss://nostream.unift.xyz","wss://jp-relay-nostr.invr.chat","wss://nostr.nokotaro.com","wss://nostr.dumpit.top","wss://nostr.test.aesyc.io","wss://nostr.malin.onl","wss://relay.humanumest.social","wss://relay.nostr.amane.moe","wss://nostr.21crypto.ch","wss://nostr.mjex.me","wss://slick.mjex.me","wss://nostr.21l.st","wss://nostr-pub.liujiale.me","wss://nos.qghs.in","wss://nostream.lucas.snowinning.com","wss://nostr.bybieyang.com","wss://nostream.frank.snowinning.com","wss://nostr.fennel.org:7000","wss://nostr-relay.aapi.me","wss://nostr-relay.nokotaro.com","wss://nostr.minimue81.selfhost.co","wss://paid.spore.ws","wss://nostr.notmyhostna.me","wss://nostr.vpn1.codingmerc.com","wss://relay.arsip.my.id","wss://nostr.buythisdip.com","wss://arnostr.permadao.io","wss://rsr.uyky.net:30443","wss://nostr.web3infra.xyz","wss://nostr.freefrom.fi","wss://nostr.l00p.org","wss://relay-1.arsip.my.id","wss://nostrafrica.pcdkd.fyi","wss://nostr.forecastdao.com","wss://quirky-bunch-isubghsvoi26fbbt3n7o.wnext.app","wss://relay.21baiwan.com","wss://relay.nostr.blockhenge.com","wss://nostr.1729.cloud","wss://relay.reeve.cn","wss://nostr.monostr.com","wss://cheery-paddock-rsakdrtc35c55n6yregn.wnext.app","wss://nostr.geekgalaxy.com","wss://nostr.risa.zone","wss://lightningrelay.com","wss://no-str.wnhefei.cn:28443","wss://relay.nostr.or.jp","wss://nostr-sg.com","wss://nostr.doufu-tech.com","wss://15171031.688.org","wss://bitcoinmaximalists.online","wss://nostr.rocket-tech.net","wss://arsip.ddns.net","wss://free-relay.nostrich.land","wss://nostream.madbean.snowinning.com","wss://nostr.nostrelay.org","wss://nostr.herci.one","wss://nostrrelay.maciejz.net","wss://nostr-2.afarazit.eu","wss://nostr.lightning.contact","wss://nostr.itredneck.com","wss://nostream-relay-nostr.831.pp.ua","wss://relay.nostr.net.in","wss://nostr.jiashanlu.synology.me","wss://private.red.gb.net","wss://nostream.dev.kronkltd.net","wss://nostr.thibautrey.fr","wss://nostr.walletofsatoshi.com","wss://relay.nostrid.com","wss://nostr.kawagarbo.xyz","wss://relay.nostr3.io","wss://nostr-relay.xbytez.io","wss://nostr.fluidtrack.in","wss://relay.nosbin.com","wss://rasca.asnubes.art","wss://nostr.beta3.dev","wss://nostr.uthark.com","wss://nostr.cruncher.com","wss://relay.jig.works","wss://nostr.foundrydigital.com","wss://nostr.chainofimmortals.net","wss://relay.nostrcheck.me","wss://nostr.rbel.co","wss://nostro.online","wss://nostr.jatm.link","wss://nostr2.rbel.co","wss://relay.nostr.vet","wss://nostr-relay.app.ikeji.ma","wss://nostro.cc","wss://nostr.yuv.al","wss://nostr.zxcvbn.space","wss://relay.lacosanostr.com","wss://lbrygen.xyz","wss://spicy-tray-3ghp3voydiwvmfm2ijur.wnext.app","wss://nostr.robotesc.ro","wss://relay.nostrdocs.com","wss://nostrue.com","wss://nostr.danvergara.com","wss://nostr.ownbtc.online","wss://n.xmr.se","wss://nostr-us.coinfundit.com","wss://nostr-eu.coinfundit.com","wss://nostramsterdam.vpx.moe","wss://alphapanda.pro","wss://nproxy.kristapsk.lv","wss://nstrs.fly.dev","wss://nostr.zue.news","wss://fiatdenier.com","wss://nostr.topeth.info","wss://nostr.klabo.blog","wss://nostr.globals.fans","wss://nostr-mv.ashiroid.com","wss://nostr.mwmdev.com","wss://nostr-dev.wellorder.net","wss://public.nostr.swissrouting.com","wss://relay.orange-crush.com","wss://nostr.bitcoinbay.engineering","wss://nostr.spaceshell.xyz","wss://nostr.fediverse.jp","wss://nostr.screaminglife.io","wss://nostr.roundrockbitcoiners.com","wss://relay.f7z.io","wss://nostr.shawnyeager.net","wss://nostr.lu.ke","wss://nostr.arguflow.gg","wss://nostr.sectiontwo.org","wss://nostr-au.coinfundit.com","wss://relay.nostrology.org"]
#DEFAULT_RELAY_API = requests.get('https://api.nostr.watch/v1/online').json()

'''

DEFAULT_RELAY=["wss://relay.damus.io","wss://nostr.wine", "wss://offchain.pub"]

''' 
>>> from nostr.key import PublicKey
>>> x = PublicKey.from_bech32('npub1cf3zeytdnwgwzz5pk2ax0vvmmlzad03xcft4d50ejrfhsh8pxcdsefx7gk')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: type object 'PublicKey' has no attribute 'from_bech32'
>>> x = PublicKey.from_npub('npub1cf3zeytdnwgwzz5pk2ax0vvmmlzad03xcft4d50ejrfhsh8pxcdsefx7gk')
>>> x.hex()
'c2622c916d9b90e10a81b2ba67b19bdfc5d6be26c25756d1f990d3785ce1361b'
'''
#0000000033f569c7069cdec575ca000591a31831ebb68de20ed9fb783e3fc287
#'since':int((datetime.strptime('2023-02-05 09:00', '%Y-%m-%d %H:%M').timestamp())),

nico_follows= []


async def one_off_query_by_pub(relay=DEFAULT_RELAY):
    """
    doing a basic query using with to manage context
    :param relay:
    :return:
    """

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



#async def main():
    #await one_off_query_by_pub()
    #await followers_follows()
    #await followers_follows2()



#if __name__ == "__main__":
#    logging.getLogger().setLevel(logging.DEBUG)
#    asyncio.run(main())



conn = ConnectingToDB(DBParams)
cursor = conn.cursor()
#print(select count (distinct follows_plus)
cursor.execute("SELECT DISTINCT follows_l3_pub FROM follows_l3")
follows_plus = cursor.fetchall()
#print(len(follows_plus))
nico_pub = ['0000000033f569c7069cdec575ca000591a31831ebb68de20ed9fb783e3fc287']


#for x in range(len(follows_plus)):
#     print('#' + str(x)+ ':  '+ PublicKey(bytes.fromhex(follows_plus[x][0])).bech32())

#print(follows_plus[25808][0])
#print(PublicKey(bytes.fromhex(follows_plus[25808][0])).bech32())
''' 
for x in follows_plus:
    try:
        print(PublicKey(bytes.fromhex(x[0])).bech32())
        cursor.execute("INSERT INTO public.follows_plus (user_pub, follows_pub, follows_plus_bech32) VALUES('{}', '{}', '{}');".format(nico_pub[0], x[0], PublicKey(bytes.fromhex(x[0])).bech32()))
    except:
        print('Duplicated FollowsPlus:' + str(PublicKey(bytes.fromhex(x[0])).bech32()))
conn.commit()
conn.close()
'''

conn = ConnectingToDB(DBParams)
cursor = conn.cursor()
cursor.execute("SELECT * from public.follows_plus")
nico = pd.DataFrame(cursor.fetchall())
print(nico.head())