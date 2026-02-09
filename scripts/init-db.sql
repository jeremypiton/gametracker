CREATE TABLE IF NOT EXISTS PLAYERS(
    player_id INT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(200),
    registration_date DATE,
    country VARCHAR(100),
    level INT
);

CREATE TABLE IF NOT EXISTS SCORES(
    score_id VARCHAR(20) PRIMARY KEY,
    player_id INT,
    game VARCHAR(100),
    score INT,
    duration_minutes INT,
    played_at DATETIME,
    platform VARCHAR(50),
    FOREIGN KEY (player_id) REFERENCES PLAYERS(player_id)
);