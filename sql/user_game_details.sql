-- command to execute sql file : psql -h hostname -p port_number -U username -f your_file.sql databasename 

DROP TABLE IF EXISTS user_game_details;

CREATE TABLE IF NOT EXISTS user_game_details (
	id                serial,                       -- used as alternative to auto increment which cannot be used in postgres  
	username          varchar(80) NOT NULL,
	game              varchar(80) NOT NULL,
	difficulty		  varchar(80) NOT NULL,
	games_won         int DEFAULT 0,
	games_lost        int DEFAULT 0,
	CONSTRAINT username_fk FOREIGN KEY (username) REFERENCES user_details(username) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS user_game_details_username_idx ON user_game_details(username);
CREATE INDEX IF NOT EXISTS user_game_details_game_idx ON user_game_details(game);