import random
from database import execute_query, fetch_data

# Drop all tables if they exist
execute_query("""
    DROP TABLE IF EXISTS game_participants;
    DROP TABLE IF EXISTS games;
    DROP TABLE IF EXISTS users;
""")

# Create tables if they do not exist
execute_query("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        kills INTEGER NOT NULL DEFAULT 0,
        best_hit INTEGER NOT NULL DEFAULT 0,
        games_played INTEGER NOT NULL DEFAULT 0,
        wins INTEGER NOT NULL DEFAULT 0
    )
""")

execute_query("""
    CREATE TABLE IF NOT EXISTS games (
        id SERIAL PRIMARY KEY,
        winner_id INTEGER REFERENCES users(id),
        start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        end_time TIMESTAMP,
        total_participants INTEGER NOT NULL DEFAULT 0
    )
""")

execute_query("""
    CREATE TABLE IF NOT EXISTS game_participants (
        game_id INTEGER REFERENCES games(id),
        user_id INTEGER REFERENCES users(id),
        placement INTEGER,
        damage_dealt INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (game_id, user_id)
    )
""")

# Sample data
usernames = [f'user_{i}' for i in range(1, 11)]
kills = [random.randint(0, 100) for _ in range(10)]
best_hits = [random.randint(0, 100) for _ in range(10)]

# Insert users
for username, kill, best_hit in zip(usernames, kills, best_hits):
    execute_query(
        "INSERT INTO users (username, kills, best_hit) VALUES (%s, %s, %s) ON CONFLICT (username) DO NOTHING",
        (username, kill, best_hit)
    )

# Get user IDs
user_ids = [row['id'] for row in fetch_data("SELECT id FROM users")]

# Insert games and participants
for i in range(1, 6):  # 5 games
    winner_id = random.choice(user_ids)
    participants = random.sample(user_ids, random.randint(2, len(user_ids)))  # Random number of participants
    game_id = execute_query(
        "INSERT INTO games (winner_id, total_participants) VALUES (%s, %s) RETURNING id",
        (winner_id, len(participants))
    )
    if game_id:
        for placement, user_id in enumerate(participants, 1):
            damage_dealt = random.randint(0, 1000)
            execute_query(
                "INSERT INTO game_participants (game_id, user_id, placement, damage_dealt) VALUES (%s, %s, %s, %s)",
                (game_id, user_id, placement, damage_dealt)
            )

print("Sample data inserted successfully.")