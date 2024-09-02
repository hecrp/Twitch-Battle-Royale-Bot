import psycopg2
from psycopg2.extras import RealDictCursor
from config import DATABASE_CONFIG

def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn

def fetch_data(query, params=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def execute_query(query, params=None):
    conn = get_db_connection()
    cur = conn.cursor()
    
    last_id = None
    try:
        cur.execute(query, params)
        
        if query.strip().upper().startswith('INSERT'):
            if 'RETURNING' not in query.upper():
                table_name = query.split()[2]
                if table_name.lower() != 'game_participants':
                    query = f"{query} RETURNING id"
                    cur.execute(query, params)
                    result = cur.fetchone()
                    if result:
                        last_id = result[0]
        
        conn.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    
    return last_id