from .db_utils import *

def select_records():
#find the region which has totalsales greater than 10000
    query = """
    SELECT region, 
	   SUM(final_amount) AS tot_sales
	   FROM transactions
	   GROUP BY region
	   HAVING SUM(final_amount)>10000;
    """
    rows, _ = execute_query(query, fetch=True)

    for row in rows:
        print(row)

def update_records():
    query = """
    UPDATE transactions
    SET discount_percent = ?
    WHERE region = ?
    """

    _, count = execute_query(query, (20, "North"))

    print(f"{count} row(s) updated.")

def delete_records():
    query = """
    DELETE FROM transactions
    WHERE final_amount < ?
    """

    _, count = execute_query(query, (100,))

    print(f"{count} row(s) deleted.")

if __name__ == "__main__":
    select_records()
    update_records()
    delete_records()