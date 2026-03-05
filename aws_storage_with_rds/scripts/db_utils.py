from config.connection import *

def execute_query(query, params=(), fetch=False):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)

    if fetch:
        result = cursor.fetchall()
        row_count = len(result)
    else:
        conn.commit()
        row_count = cursor.rowcount
        result = None

    cursor.close()
    conn.close()

    return result, row_count