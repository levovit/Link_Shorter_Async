create table links
(
	id serial not null
		constraint links_pk
			primary key,
	long_link text,
	short_link text,
	user_name text default 'anon'::text,
	active_until timestamp default (CURRENT_TIMESTAMP + '90 days'::interval),
	active boolean default true
);

alter table links owner to postgres;

create unique index links_id_uindex
	on links (id);

INSERT INTO links
values (default, 'https://www.google.com.ua/webhp?authuser=1', 'www.google.com.ua', 'levovit', default, default);
