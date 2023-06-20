import sqlite3
from typing import Dict, Optional

# Create a database connection
def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect(':memory:')  # creates a memory database for demo purposes
        return conn
    except Exception as e:
        print(e)

# Function to execute a generic SQL statement
def execute_sql(conn, sql: str, params: Optional[Dict] = None):
    try:
        cur = conn.cursor()
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        return cur.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")

# CRUD operations
def select(conn, table_id: str, params: Optional[Dict] = None, select_col: Optional[str] = None, where_clause: str = ""):
    query = f"SELECT {select_col or '*'} FROM {table_id} {where_clause}"
    return execute_sql(conn, query, params)

def insert(conn, table_id: str, params: Dict):
    fields = ', '.join(params.keys())
    placeholders = ', '.join(['?' for _ in params.keys()])
    query = f"INSERT INTO {table_id} ({fields}) VALUES ({placeholders})"
    execute_sql(conn, query, list(params.values()))

def update(conn, table_id: str, params: Dict, where_clause: str):
    set_clause = ', '.join([f"{key} = ?" for key in params.keys()])
    query = f"UPDATE {table_id} SET {set_clause} WHERE {where_clause}"
    execute_sql(conn, query, list(params.values()))

def delete(conn, table_id: str, where_clause: str):
    query = f"DELETE FROM {table_id} WHERE {where_clause}"
    execute_sql(conn, query)
