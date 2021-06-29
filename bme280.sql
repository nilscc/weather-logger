create schema if not exists bme280;
set search_path = bme280;

begin;

    create table if not exists t_bme280
    (
        id              bigserial primary key,
        date            timestamp not null default now(),
        temperature     double precision,
        humidity        double precision,
        pressure        double precision,

        unique(date)
    );

commit;
