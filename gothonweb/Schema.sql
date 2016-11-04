CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	name TEXT,
	_pass TEXT,
	gothonweb INTEGER,
	piclink TEXT DEFAULT 'default.jpg',
)

# Dropped it
CREATE TABLE score_board (
	id INTEGER PRIMARY KEY,
	user_id INT, 
	game TEXT, 
	score INTEGER
)
