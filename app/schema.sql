drop table if exists files;
drop table if exists chat_log;

create table files (
  passcode integer primary key,
  file_name text not null,
  opener_email text not null,
  open_date text not null
);

create table chat_log (
  chat_id integer primary key autoincrement,
  passcode integer,
  user_email text not null,
  message text not null,
  chat_date text not null,
  foreign key(passcode) references files(passcode)
);
