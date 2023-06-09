create table location (
  id bigint primary key generated always as identity,
  created_at timestamp default now(),
  lat float8,
  lng float8,
  name text
);

create table trip (
  id bigint primary key generated always as identity,
  created_at timestamp default now(),
  name text,
  user_id text
);

create table photos (
  id bigint primary key generated always as identity,
  created_at timestamp default now(),
  location_id bigint references location (id),
  url text
);

create table posts (
  id bigint primary key generated always as identity,
  created_at timestamp default now(),
  location_id bigint references location (id),
  post text
);

create table route (
  id bigint primary key generated always as identity,
  created_at timestamp default now(),
  name text,
  trip bigint references trip (id)
);

create table route_has_location (
  created_at timestamp default now(),
  route_id bigint references route (id),
  location_id bigint references location (id),
  "index" bigint not null,
  PRIMARY KEY(route_id, location_id, "index")
);

create table shared_trips (
  trip_id bigint references trip (id),
  user_id text,
  created_at timestamp default now(),
  PRIMARY KEY(trip_id, user_id)
);

insert into storage.buckets
  (id, name)
values
  ('photos', 'photos');
