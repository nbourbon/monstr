import logging
import asyncio
from monstr.client.client import Client, ClientPool
from monstr.client.event_handlers import PrintEventHandler
from monstr.event.event import Event
from monstr.encrypt import Keys
import string
from nostr.key import PublicKey


#export PYTHONPATH="$PYTHONPATH:./"

DEFAULT_RELAY= ["wss://rsslay.ch3n2k.com",
"wss://nostr.21sats.net",
"wss://nostr.rocketnode.space",
"wss://relay.nostr.bg",
"wss://nostr.zoomout.chat",
"wss://nostr.malin.onl",
"wss://nostr.reamde.dev",
"wss://nostr-01.dorafactory.org",
"wss://relay.nostr-latam.link",
"wss://nostr.globals.fans",
"wss://nostr.oxtr.dev",
"wss://nostr.fractalized.ovh",
"wss://rsslay.data.haus",
"wss://nostr.primz.org",
"wss://nostr.minimue81.selfhost.co",
"wss://relay.nostr.au",
"wss://nostr.21m.fr",
"wss://relay.nostrprotocol.net",
"wss://nostr-bg01.ciph.rs",
"wss://nostr-relay.usebitcoin.space",
"wss://btc.klendazu.com",
"wss://relay.n057r.club",
"wss://nostr.vpn1.codingmerc.com",
"wss://nostr.jatm.link",
"wss://nostr.yael.at",
"wss://nostr.jacany.com",
"wss://nos.qghs.in",
"wss://15171031.688.org",
"wss://nostream.dev.kronkltd.net",
"wss://nostr.ownscale.org",
"wss://relay.cent2sat.com",
"wss://relay.nostr.ch",
"wss://no-str.org",
"wss://btcpay.kukks.org/nostr/ws"]


import requests
#DEFAULT_RELAY = requests.get('https://api.nostr.watch/v1/online').json()
'''
#Long list of relays
DEFAULT_RELAY=["wss://relay.damus.io","wss://eden.nostr.land","wss://brb.io", "wss://nostr.mutinywallet.com", "wss://relay.snort.social","wss://nostr.milou.lol", "wss://puravida.nostr.land", "wss://relay.nostr.bg","wss://relay.honk.pw","wss://nostr-pub.wellorder.net","wss://nostr.mom","wss://nostr.sandwich.farm","wss://nostr.slothy.win","wss://global.relay.red","wss://relay.stoner.com","wss://nostr.einundzwanzig.space","wss://nostr.cercatrova.me","wss://nostr.swiss-enigma.ch","wss://relay.nostr-latam.link","wss://nostr.phenomenon.space","wss://nos.lol","wss://relay.current.fyi","wss://relay.nostr.band","wss://nostr-relay.derekross.me","wss://nostr.developer.li","wss://no.str.cr","wss://nostr.bongbong.com","wss://relay.sendstr.com","wss://relay.cryptocculture.com","wss://relay.nostr.scot","wss://nostr.hackerman.pro","wss://nostr.blockchaincaffe.it","wss://relay.taxi","wss://nostr.kollider.xyz","wss://nostr.massmux.com","wss://nostr.relayer.se","wss://nostr.ethtozero.fr","wss://nostr-relay.digitalmob.ro","wss://blg.nostr.sx","wss://no.str.watch","wss://nostr-relay.schnitzel.world","wss://nostr1.tunnelsats.com","wss://nostr.radixrat.com","wss://relay.t5y.ca","wss://relay.nostr.com.au","wss://knostr.neutrine.com","wss://nostr.nodeofsven.com","wss://relay.n057r.club","wss://nostrical.com","wss://nostr-relay.freedomnode.com","wss://nostr.jimc.me","wss://nostr.gromeul.eu","wss://node01.nostress.cc","wss://relay.nostr.ro","wss://relay.nostrich.de","wss://nostr.mustardnodes.com","wss://nostr-bg01.ciph.rs","wss://nostr.vulpem.com","wss://relay.ryzizub.com","wss://nostr3.actn.io","wss://nostr.bostonbtc.com","wss://nostr.bch.ninja","wss://nostr-verif.slothy.win","wss://nostr.supremestack.xyz","wss://relay.lexingtonbitcoin.org","wss://relay.nostr.moe","wss://nostr-1.nbo.angani.co","wss://nostr.zoomout.chat","wss://nostr.coollamer.com","wss://nostr.thesimplekid.com","wss://relay.nostr.express","wss://nostr.blocs.fr","wss://nostr.8e23.net","wss://nostr.rdfriedl.com","wss://nostr.shmueli.org","wss://btc.klendazu.com","wss://nostr.sabross.xyz","wss://nostr2.actn.io","wss://relay.plebstr.com","wss://nostr.uselessshit.co","wss://nostr.adpo.co","wss://relay.wellorder.net","wss://nostr.handyjunky.com","wss://relay-pub.deschooling.us","wss://nostr.satsophone.tk","wss://nostr.easydns.ca","wss://relay.dwadziesciajeden.pl","wss://nostr-relay.gkbrk.com","wss://nostr-pub1.southflorida.ninja","wss://relay.orangepill.dev","wss://nostr.600.wtf","wss://zur.nostr.sx","wss://nostr.mouton.dev","wss://e.nos.lol","wss://relay.nostr.vision","wss://nostrich.friendship.tw","wss://relay.nostrzoo.com","wss://nostream-production-5895.up.railway.app","wss://nostream.nostr.parts","wss://nostr.bitcoin.sex","wss://nostr-relay.texashedge.xyz","wss://nostr.thomascdnns.com","wss://nostr.btcmp.com","wss://relay.nostr.africa","wss://ragnar-relay.com","wss://nostr.zkid.social","wss://nostr.bitcoin-21.org","wss://nostr.com.de","wss://eosla.com","wss://nostr.data.haus","wss://relay1.gems.xyz","wss://nostrpro.xyz","wss://relay.austrich.net","wss://nostr.terminus.money","wss://nostr.0ne.day","wss://relay.valera.co","wss://nostr.sg","wss://nostr.liberty.fans","wss://nostr.cro.social","wss://nostr01.opencult.com","wss://nostr.ltbl.io","wss://nostr.reamde.dev","wss://nostr.wine","wss://nostr.koning-degraaf.nl","wss://nostr.pleb.network","wss://nostr.cheeserobot.org","wss://nostr.thank.eu","wss://relay.hamnet.io","wss://nostr.shroomslab.net","wss://relay.zhix.in","wss://nostr.primz.org","wss://nostr.truckenbucks.com","wss://nostr.rajabi.ca","wss://zee-relay.fly.dev","wss://nostr.blockpower.capital","wss://eospark.com","wss://nostr.sidnlabs.nl","wss://nostr-rs-relay.cryptoassetssubledger.com","wss://nostr.inosta.cc","wss://nostr21.com","wss://arc1.arcadelabs.co","wss://nostr.nym.life","wss://relay.nostr.distrl.net","wss://relay.zeh.app","wss://ch1.duno.com","wss://spore.ws","wss://relay.727whisky.com","wss://nostr.ch3n2k.com","wss://nostr.island.network","wss://cloudnull.land","wss://relay.nostrati.com","wss://relay-dev.cowdle.gg","wss://nostr.ginuerzh.xyz","wss://nostr.nakamotosatoshi.cf","wss://relay.1bps.io","wss://nostr1.saftup.xyz","wss://relay.nostrview.com","wss://relay.nostromo.social","wss://1.noztr.com","wss://offchain.pub","wss://nostr.nikolaj.online","wss://nostr-relay.pcdkd.fyi","wss://relay.nostr.wirednet.jp","wss://nostrsxz4lbwe-nostr.functions.fnc.fr-par.scw.cloud","wss://www.131.me","wss://nostream.unift.xyz","wss://jp-relay-nostr.invr.chat","wss://nostr.nokotaro.com","wss://nostr.dumpit.top","wss://nostr.test.aesyc.io","wss://nostr.malin.onl","wss://relay.humanumest.social","wss://relay.nostr.amane.moe","wss://nostr.21crypto.ch","wss://nostr.mjex.me","wss://slick.mjex.me","wss://nostr.21l.st","wss://nostr-pub.liujiale.me","wss://nos.qghs.in","wss://nostream.lucas.snowinning.com","wss://nostr.bybieyang.com","wss://nostream.frank.snowinning.com","wss://nostr.fennel.org:7000","wss://nostr-relay.aapi.me","wss://nostr-relay.nokotaro.com","wss://nostr.minimue81.selfhost.co","wss://paid.spore.ws","wss://nostr.notmyhostna.me","wss://nostr.vpn1.codingmerc.com","wss://relay.arsip.my.id","wss://nostr.buythisdip.com","wss://arnostr.permadao.io","wss://rsr.uyky.net:30443","wss://nostr.web3infra.xyz","wss://nostr.freefrom.fi","wss://nostr.l00p.org","wss://relay-1.arsip.my.id","wss://nostrafrica.pcdkd.fyi","wss://nostr.forecastdao.com","wss://quirky-bunch-isubghsvoi26fbbt3n7o.wnext.app","wss://relay.21baiwan.com","wss://relay.nostr.blockhenge.com","wss://nostr.1729.cloud","wss://relay.reeve.cn","wss://nostr.monostr.com","wss://cheery-paddock-rsakdrtc35c55n6yregn.wnext.app","wss://nostr.geekgalaxy.com","wss://nostr.risa.zone","wss://lightningrelay.com","wss://no-str.wnhefei.cn:28443","wss://relay.nostr.or.jp","wss://nostr-sg.com","wss://nostr.doufu-tech.com","wss://15171031.688.org","wss://bitcoinmaximalists.online","wss://nostr.rocket-tech.net","wss://arsip.ddns.net","wss://free-relay.nostrich.land","wss://nostream.madbean.snowinning.com","wss://nostr.nostrelay.org","wss://nostr.herci.one","wss://nostrrelay.maciejz.net","wss://nostr-2.afarazit.eu","wss://nostr.lightning.contact","wss://nostr.itredneck.com","wss://nostream-relay-nostr.831.pp.ua","wss://relay.nostr.net.in","wss://nostr.jiashanlu.synology.me","wss://private.red.gb.net","wss://nostream.dev.kronkltd.net","wss://nostr.thibautrey.fr","wss://nostr.walletofsatoshi.com","wss://relay.nostrid.com","wss://nostr.kawagarbo.xyz","wss://relay.nostr3.io","wss://nostr-relay.xbytez.io","wss://nostr.fluidtrack.in","wss://relay.nosbin.com","wss://rasca.asnubes.art","wss://nostr.beta3.dev","wss://nostr.uthark.com","wss://nostr.cruncher.com","wss://relay.jig.works","wss://nostr.foundrydigital.com","wss://nostr.chainofimmortals.net","wss://relay.nostrcheck.me","wss://nostr.rbel.co","wss://nostro.online","wss://nostr.jatm.link","wss://nostr2.rbel.co","wss://relay.nostr.vet","wss://nostr-relay.app.ikeji.ma","wss://nostro.cc","wss://nostr.yuv.al","wss://nostr.zxcvbn.space","wss://relay.lacosanostr.com","wss://lbrygen.xyz","wss://spicy-tray-3ghp3voydiwvmfm2ijur.wnext.app","wss://nostr.robotesc.ro","wss://relay.nostrdocs.com","wss://nostrue.com","wss://nostr.danvergara.com","wss://nostr.ownbtc.online","wss://n.xmr.se","wss://nostr-us.coinfundit.com","wss://nostr-eu.coinfundit.com","wss://nostramsterdam.vpx.moe","wss://alphapanda.pro","wss://nproxy.kristapsk.lv","wss://nstrs.fly.dev","wss://nostr.zue.news","wss://fiatdenier.com","wss://nostr.topeth.info","wss://nostr.klabo.blog","wss://nostr.globals.fans","wss://nostr-mv.ashiroid.com","wss://nostr.mwmdev.com","wss://nostr-dev.wellorder.net","wss://public.nostr.swissrouting.com","wss://relay.orange-crush.com","wss://nostr.bitcoinbay.engineering","wss://nostr.spaceshell.xyz","wss://nostr.fediverse.jp","wss://nostr.screaminglife.io","wss://nostr.roundrockbitcoiners.com","wss://relay.f7z.io","wss://nostr.shawnyeager.net","wss://nostr.lu.ke","wss://nostr.arguflow.gg","wss://nostr.sectiontwo.org","wss://nostr-au.coinfundit.com","wss://relay.nostrology.org"]
'''
#DEFAULT_RELAY=["wss://brb.io", "wss://relay.damus.io","wss://eden.nostr.land","wss://brb.io"]

import psycopg2 #librería para conectar al Postgresql
import pandas as pd
#DEFAULT_RELAY=["wss://relay.snort.social"]

def ConnectingToDB(DBParams):
    return(psycopg2.connect(database=DBParams['database'], user=DBParams['user'], password=DBParams['password'],host=DBParams['host'], port= DBParams['port']))

DBParams = {'database':'postgres', 'user':'postgres', 'password':'postgres', 'host':'localhost', 'port':'5432'}

from datetime import datetime

conn = ConnectingToDB(DBParams)
cursor = conn.cursor()
cursor.execute("SELECT follows_pub FROM follows_plus")
follows = cursor.fetchall()
nico_follows = []

for x in follows:
#for x in ['0000000033f569c7069cdec575ca000591a31831ebb68de20ed9fb783e3fc287']:

    t= all(c in string.hexdigits for c in x[0])
    if t==True:
        nico_follows.append(x[0])
    else:
        if len(x[0]) == 63:
            pub = PublicKey.from_npub(x[0])
            nico_follows.append(pub.hex())
        else:
            pass

async def one_off_query_by_pub(relay, authors):
    """
    doing a basic query using with to manage context
    :param relay:
    :return:
    """

    conn = ConnectingToDB(DBParams)
    cursor = conn.cursor()
    beg=0
    end=0
    for r in relay:
        for i in range(500, len(authors), 500):
            if len(authors)-i>500:
                beg=i-500
                end=i
            else:
                beg:i
                end:None
            async with Client(r) as c:
                events = await c.query({
                    #'kinds':[7,1],
                    'authors': authors[beg:end],
                    'since':int((datetime.strptime('2023-02-01 00:00', '%Y-%m-%d %H:%M').timestamp()))
                })

                for c_evt in events:
                    try:
                        cursor.execute("INSERT INTO public.events (relay_url, id,kind, content, pub_key, created_at) VALUES('{}', '{}', '{}', '{}', '{}','{}');".format(r,c_evt.id, c_evt.kind, c_evt.content.replace("'", "''"), c_evt.pub_key, c_evt.created_at))
                    except:
                        print('duplicated event')
                conn.commit()
    conn.close()



l=len(nico_follows)
async def main():
    for x in DEFAULT_RELAY:
        r = [x]
        try:
            await one_off_query_by_pub(relay=r, authors=nico_follows)
        except:
            print('Couldn''t Connect to: '+ str(x))


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    asyncio.run(main())



async def one_off_query_by_pub(relay, authors):
    """
    doing a basic query using with to manage context
    :param relay:
    :return:
    """

    conn = ConnectingToDB(DBParams)
    cursor = conn.cursor()
    beg=0
    end=0
    for r in relay:
        for i in range(500, len(authors), 500):
            if len(authors)-i>500:
                beg=i-500
                end=i
            else:
                beg:i
                end:None
            try:
                async with asyncio.wait_for(Client(r).query({
                        'authors': authors[beg:end],
                        'since':int((datetime.strptime('2023-02-01 00:00', '%Y-%m-%d %H:%M').timestamp()))
                    }), timeout=10) as events:

                    for c_evt in events:
                        try:
                            cursor.execute("INSERT INTO public.events (relay_url, id,kind, content, pub_key, created_at) VALUES('{}', '{}', '{}', '{}', '{}','{}');".format(r,c_evt.id, c_evt.kind, c_evt.content.replace("'", "''"), c_evt.pub_key, c_evt.created_at))
                        except:
                            print('duplicated event')
                    conn.commit()
            except asyncio.TimeoutError:
                print(f"Timed out while connecting to relay {r}")
                continue
            except Exception as e:
                print(f"Failed to connect to relay {r}: {str(e)}")
                continue
    conn.close()
