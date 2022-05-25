CREATE TABLE STATISTICS(
    id uuid primary key,
    event_date date notnull,
    views bigint default 0 check ( views >= 0 ),
    clicks bigint default 0 check ( clicks >= 0 ),
    cost decimal(20, 2) default 0.00 check ( cost >= 0 )
)