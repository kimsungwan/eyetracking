import sqlite3
import pandas as pd

def inspect_users():
    try:
        # Connect to the database
        conn = sqlite3.connect('users.db')
        
        # Query all users
        query = "SELECT * FROM users"
        
        # Use pandas to print it nicely
        df = pd.read_sql_query(query, conn)
        
        if df.empty:
            print("No users found in the database.")
        else:
            print("=== Current Users in Database ===")
            print(df.to_string(index=False))
            
        conn.close()
        
    except Exception as e:
        print(f"Error inspecting database: {e}")

if __name__ == "__main__":
    inspect_users()
