CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	username VARCHAR(25) UNIQUE,
	hashed_password VARCHAR(200),
	role VARCHAR(15)
);

CREATE TABLE games (
	id SERIAL PRIMARY KEY ,
	world VARCHAR(40) NOT NULL,
	dm_id INT NOT NULL,
	FOREIGN KEY (dm_id) REFERENCES players(id)
);

CREATE TABLE characters (
	id SERIAL PRIMARY KEY,
	name VARCHAR(25) UNIQUE,
    character_class VARCHAR(25),
    level INT, 
    race VARCHAR(25),
    current_exp INT NOT NULL CHECK (current_exp >= 0),
    strength INT NOT NULL CHECK (strength >=1 and strength <=20),
    dexterity INT NOT NULL CHECK (dexterity >=1 and dexterity <=20),
    constitution INT NOT NULL CHECK (constitution >=1 and constitution <=20),
    intelligence INT NOT NULL CHECK (intelligence >=1 and intelligence <=20),
    wisdom INT NOT NULL CHECK (wisdom >=1 and wisdom <=20),
    charisma INT NOT NULL CHECK (charisma >=1 and charisma <=20),
    alive BOOL NOT NULL,
    owner_id INT NOT NULL,
	game_id INT NOT NULL,
	FOREIGN KEY (owner_id) REFERENCES players(id),
	FOREIGN KEY (game_id) REFERENCES games(id),
	CONSTRAINT level_check CHECK (level>=1 and level <=20)
);