from database import execute_query, fetch_data

def get_users():
    query = "SELECT * FROM users"
    return fetch_data(query)

def get_games():
    query = "SELECT * FROM games"
    return fetch_data(query)

def get_user_stats():
    query = """
    SELECT u.username, COUNT(gp.game_id) as games_played, u.kills as total_kills, u.best_hit, u.wins
    FROM users u
    LEFT JOIN game_participants gp ON u.id = gp.user_id
    GROUP BY u.id
    ORDER BY total_kills DESC
    """
    return fetch_data(query)

def get_recent_games(limit=5):
    query = """
    SELECT g.id, g.start_time as created_at, u.username as winner, g.total_participants
    FROM games g
    JOIN users u ON g.winner_id = u.id
    ORDER BY g.start_time DESC
    LIMIT %s
    """
    return fetch_data(query, (limit,))