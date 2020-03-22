
echo ".open db.sqlite3" | sqlite3
sqlite3 db.sqlite3 "CREATE TABLE IF NOT EXISTS "dosuke_config" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "key" varchar(20) NOT NULL, "value" text NOT NULL, "memo" text NULL);"

sqlite3 db.sqlite3 "insert into dosuke_config values(1,'session_start','14','');"
sqlite3 db.sqlite3 "insert into dosuke_config values(2,'session_end','20','');"
sqlite3 db.sqlite3 "insert into dosuke_config values(3,'room_start','0','');"
sqlite3 db.sqlite3 "insert into dosuke_config values(4,'room_end','27','');"
sqlite3 db.sqlite3 "insert into dosuke_config values(5,'max_days','4','');"
