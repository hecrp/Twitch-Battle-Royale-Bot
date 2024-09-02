import psycopg2
from config import DATABASE_CONFIG

def create_tables():
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        # Create database if it doesn't exist
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DATABASE_CONFIG['dbname'],))
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {DATABASE_CONFIG['dbname']}")
            print(f"Database '{DATABASE_CONFIG['dbname']}' created successfully")

        # Switch to the new database
        conn.close()
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()

        # Create user if it doesn't exist
        cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (DATABASE_CONFIG['user'],))
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE USER {DATABASE_CONFIG['user']} WITH PASSWORD '{DATABASE_CONFIG['password']}'")
            print(f"User '{DATABASE_CONFIG['user']}' created successfully")

        # Grant privileges to the user
        cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DATABASE_CONFIG['dbname']} TO {DATABASE_CONFIG['user']}")
        cur.execute(f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {DATABASE_CONFIG['user']}")
        cur.execute(f"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO {DATABASE_CONFIG['user']}")
        print(f"Privileges granted to user '{DATABASE_CONFIG['user']}'")

        # Commit the changes
        conn.commit()
        # Create users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            kills INT DEFAULT 0,
            best_hit INT DEFAULT 0,
            games_played INT DEFAULT 0,
            wins INT DEFAULT 0
        )
        """)

        # Create games table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id SERIAL PRIMARY KEY,
            winner_id INT REFERENCES users(id),
            total_participants INT NOT NULL,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP
        )
        """)

        # Create game_participants table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS game_participants (
            game_id INT REFERENCES games(id),
            user_id INT REFERENCES users(id),
            placement INT,
            damage_dealt INT,
            PRIMARY KEY (game_id, user_id)
        )
        """)

        # Commit the changes
        conn.commit()
        
        print("Tables created successfully")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    create_tables()
