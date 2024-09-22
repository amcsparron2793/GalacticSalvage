create table Players(id integer primary key autoincrement,
                     player_name nvarchar(50) not null unique);

create table Leaderboard(id integer primary key autoincrement,
                         GameDate date not null default current_date,
                         player_id integer not null references Players(id),
                         score integer not null,
                         level integer not null
                         );

create view FullLeaderboard as
    select P.player_name, GameDate, score, level
    from Leaderboard
        join Players P on P.id = Leaderboard.player_id;

create view TopTenLeaderboard as
select *
from FullLeaderboard
order by score desc
limit 10
