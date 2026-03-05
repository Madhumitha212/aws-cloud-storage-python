from .db_utils import *

#aggregations
def company_summary_metrics():
    query = """
    SELECT 
        COUNT(*) AS total_transactions,
        SUM(final_amount) AS total_revenue,
        AVG(final_amount) AS avg_transaction_value
    FROM transactions;
    """

    rows, _ = execute_query(query, fetch=True)

    print("Company Summary:", rows[0])

#Regions With High Revenue & High Avg Discount
def high_performing_regions():
    query = """
    SELECT 
        region,
        SUM(final_amount) AS total_revenue,
        AVG(discount_percent) AS avg_discount
    FROM transactions
    GROUP BY region
    HAVING 
        SUM(final_amount) > ?
        AND AVG(discount_percent) > ?;
    """

    rows, _ = execute_query(query, (50000, 10), fetch=True)

    for row in rows:
        print(row)

#Last 30 days transactions
def last_30_days_transactions():
    query = """
    SELECT *
    FROM transactions
    WHERE transaction_date >= DATEADD(DAY, -30, GETDATE());
    """

    rows, row_count = execute_query(query, fetch=True)

    print("Last 30 Days Transactions:", row_count)
    for row in rows[:5]:
        print(row)

#Rank Customers by Total Spending
def rank_customers_by_spending():
    query = """
    SELECT 
        customer_id,
        SUM(final_amount) AS total_spent,
        RANK() OVER (ORDER BY SUM(final_amount) DESC) AS spending_rank
    FROM transactions
    GROUP BY customer_id;
    """

    rows, _ = execute_query(query, fetch=True)

    for row in rows:
        print(row)

#Top Performing Region
def top_performing_region():
    query = """
    SELECT 
        TOP 1
        region,
        SUM(final_amount) AS total_revenue
    FROM transactions
    GROUP BY region
    ORDER BY total_revenue DESC;
    """

    rows, _ = execute_query(query, fetch=True)

    print("Top Region:", rows[0])

if __name__ == "__main__":
    company_summary_metrics()
    high_performing_regions()
    last_30_days_transactions()
    rank_customers_by_spending()
    top_performing_region()