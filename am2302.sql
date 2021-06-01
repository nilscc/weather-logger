create schema if not exists am2302;
set search_path = am2302;

begin;

    create table if not exists t_am2302
    (
        id              bigserial primary key,
        date            timestamp not null default now(),
        temperature     double precision,
        humidity        double precision,

        unique(date)
    );

commit;
