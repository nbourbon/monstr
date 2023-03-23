--- drop table events 

CREATE TABLE public.events (
	relay_url text NOT NULL,
	id text NOT NULL,
	kind int4 NOT NULL,
	"content" text NULL,
	pub_key text NOT NULL,
	created_at timestamptz NOT NULL,
	CONSTRAINT events_relayurl_id_pk PRIMARY KEY (relay_url, id)
);

--- DROP TABLE public.follows_l1;

CREATE TABLE public.follows_l1 (
	user_pub text NOT NULL,
	follows_l1_pub text NOT NULL,
	relay_url text NOT NULL,
	created_at timestamptz NOT NULL,
	CONSTRAINT event_userpub_l1_pk PRIMARY KEY (user_pub, follows_l1_pub, relay_url, created_at)
);

-- DROP TABLE public.follows_l2;

CREATE TABLE public.follows_l2 (
	follows_l1_pub text NOT NULL,
	follows_l2_pub text NOT NULL,
	relay_url text NOT NULL,
	created_at timestamptz NOT NULL
	---CONSTRAINT event_userpub_l1_l2_pk PRIMARY KEY (follows_l1_pub, follows_l2_pub, relay_url, created_at)
);


-- DROP TABLE public.follows_l2;

CREATE TABLE public.follows_l3 (
	follows_l2_pub text NOT NULL,
	follows_l3_pub text NOT NULL,
	relay_url text NOT NULL,
	CONSTRAINT event_userpub_l2_l3_pk PRIMARY KEY (follows_l2_pub, follows_l3_pub, relay_url)
);

-- DROP TABLE public.follows_plus;

CREATE TABLE public.follows_plus (
	user_pub text NOT NULL,
	follows_pub text NOT NULL,
	follows_plus_bech32 text NOT NULL,
	CONSTRAINT followsplus_user_follow_id_pk PRIMARY KEY (user_pub, follows_pub)
);

-- DROP TABLE public.connected_relays;

CREATE TABLE public.connected_relays (
	relay_url text NOT NULL,
	step text NOT NULL,
	CONSTRAINT connectedRelays_relay_step_pk PRIMARY KEY (relay_url, step)
);

-- DROP TABLE public.checked_relays;

CREATE TABLE public.checked_relays (
	relay_url text NOT NULL,
	checked text NOT NULL,
	read_r text NOT NULL,
	CONSTRAINT checkedRelays_relay_checked_read_pk PRIMARY KEY (relay_url, checked, read_r)
);


--- drop view public.distinctrelays 
create view public.distinctRelays
as select count(distinct events.id), relay_url
from events 
where created_at between '2023-02-01 00:00' and '2023-03-15 00:00'
group by relay_url
order by count;



--- drop view public.pollination 
create view public.pollination
as select distinct e.relay_url, count (e.id) from events e 
where e.pub_key = '0000000033f569c7069cdec575ca000591a31831ebb68de20ed9fb783e3fc287' and created_at between '2023-02-01 00:00' and '2023-03-15 00:00'
group by e.relay_url 
order by count desc;  


--- drop view public.kind 
create view public.kind
as select e.kind, count (distinct e.id) from events e 
where created_at between '2023-02-01 00:00' and '2023-03-15 00:00'
group by e.kind
order by count desc  ;

--- contando pub_key con mayor cantidad de eventos
--- drop view public.toppubkeys 
create view toppubkeys 
as select count (distinct id) as nr, fp.follows_plus_bech32, pub_key 
from events e 
join follows_plus fp on e.pub_key = fp.follows_pub 
where e.created_at between '2023-02-01 00:00' and '2023-03-15 00:00'
group by distinct e.pub_key, fp.follows_plus_bech32 
order by nr desc  ;

--- drop view profiles 
--- creando perfiles con todo su detalle
create view profiles
as select e.pub_key, fp.follows_plus_bech32, cast("content" as json)->>'name' as name, cast("content" as json)->>'display_name' as disp_name, cast("content" as json)->>'picture' as pic, cast("content" as json)->>'about' as about, cast("content" as json)->>'nip05' as nip05, cast("content" as json)->>'lud06' as LNAddress, cast("content" as json)->>'banner' as banner, relay_url 
from events e
join follows_plus fp on fp.follows_pub = e.pub_key 
where kind = 0 and "content" like '{%';


