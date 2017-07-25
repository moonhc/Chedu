drop table if exists files;
drop table if exists chat_log;

create table files (
  passcode string primary key,
  file_name string not null,
  open_date string not null
);

create table chat_log (
  chat_id integer primary key autoincrement,
  passcode string not null,
  user_email string not null,
  message string not null,
  chat_date string not null,
  foreign key(passcode) references files(passcode)
);
