-- created on , modified on, username, password
-- command to execute sql file : psql -h hostname -p port_number -U username -f your_file.sql databasename 
-- username could have been used as foreign key to user_game_details only if it was a unique constraint column in user_Details table

-- CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS user_details;

CREATE TABLE IF NOT EXISTS "user_details" (	
	"id"              uuid NOT NULL PRIMARY KEY,
	"username"        varchar(80) NOT NULL,                  -- could have had UNQIUE constraint and then can be used as foreign key
	"password"		  varchar(80) NOT NULL,
	"created_on"      timestamp WITH time ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"modified_on"     timestamp WITH time ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT "username_unique" UNIQUE ("username")
);

CREATE INDEX IF NOT EXISTS user_details_username_idx ON user_details(username);
CREATE INDEX IF NOT EXISTS user_details_password_idx ON user_details(password);