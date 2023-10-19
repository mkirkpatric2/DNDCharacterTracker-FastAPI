select * from games;

INSERT INTO players (username, hashed_password, role) VALUES
('michael', '$2b$12$M8rsz5Sli8xDVYi/Zq.q5uFoPkbBD0fl.AE9veKb2w0zpoFpcSIxi', 'admin'),
('andi', '$2b$12$5aY6xWl1zd4W.99Ae48WIeH1TutwFO.6.akjQlVLe2/CgwGXD8xVe', 'admin'),
('koda', '$2b$12$00Exa8WuQr60qdUV552DfO/u7crvwSeVnnpxSGjGZz2u/d8ir4fj.', 'user'),
('jonathan', '$2b$12$6qt48xdX7BaJXdYVM1b63OkNhR4KHulBbyEQ3mcg849LmcI1GuHNS','user');

INSERT INTO games (world, dm_id) VALUES
('grand line', 1),
('ravnica', 1),
('kara-tur', 2);


-- (living characters)
INSERT INTO characters (name, character_class, level, race, current_exp, strength, 
						dexterity, constitution, intelligence, wisdom, charisma, 
						alive, owner_id, game_id)
VALUES
('Falkrunn', 'Fighter', 4, 'Dwarf', 2232, 15, 13, 16, 9, 10, 13, True, 4, 3),
('Miri Dundrake', 'Paladin', 5, 'Half-Elf', 22, 13, 8, 16, 13, 13, 8, True, 3, 3),
('Shalkashlah', 'Artificer', 4, 'Yuan-Ti', 2222, 9, 16, 8, 15, 9, 12, True, 1, 3),
('Shake Bright-Cliffs', 'Warlock', 5, 'Tabaxi', 1, 10, 11, 12, 13, 14, 15, True, 2, 2),
('Rimmon Laboda', 'Druid', 8, 'Tiefling', 24444, 14, 9, 14, 12, 19, 10, True, 3, 2),
('Ubada', 'Druid', 8, 'Orc', 2423, 11, 10, 12, 11, 20, 18, True, 4, 2),
('Borchi', 'Fighter', 3, 'Fishman', 22, 19, 15, 7, 8, 15, 7, True, 3, 1),
('Bernadinho', 'Bard', 1, 'Ex-Celestial Dragon', 6666, 8, 6, 6, 7, 11, 4, True, 4, 1),
('Olga', 'Ranger', 4, 'Human', 2341, 9, 16, 7, 8, 12, 14, True, 2, 1);

INSERT INTO characters (name, character_class, level, race, current_exp, strength, 
						dexterity, constitution, intelligence, wisdom, charisma, 
						alive, owner_id, game_id)
VALUES
('Smasher', 'Duid', 5, 'Kenku', 12345, 15, 14, 2, 15, 6, 15, False, 4, 3),
('Rose Greenleaf', 'Warlock', 4, 'Halfling', 422, 12, 9, 10, 10, 15, 12, False, 3, 3),
('Tuneer', 'Wizard', 3, 'Human', 2, 9, 8, 8, 18, 12, 12, False, 3, 1),
('Elama Qualanthri', 'Ranger', 2, 'Sea Elf', 142, 11, 15, 11, 9, 14, 14, False, 2, 2);