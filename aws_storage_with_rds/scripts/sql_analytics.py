from .db_utils import *
from .export_to_csv import *

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

    headers = [
        "total_transactions",
        "total_revenue",
        "avg_transaction_value"
    ]

    upload_query_results_to_s3(
        "analytics/company_summary.csv",
        rows,
        headers
    )

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

    headers = ["region", "total_revenue", "avg_discount"]

    # Print results
    print("High Performing Regions:")
    for row in rows:
        row_dict = dict(zip(headers, row))
        print(row_dict)

    # Upload to S3
    upload_query_results_to_s3(
        "analytics/high_performing_regions.csv",
        rows,
        headers
    )

#Last 30 days transactions
def last_30_days_transactions():
    query = """
    SELECT transaction_id, transaction_date, final_amount
    FROM transactions
    WHERE transaction_date >= DATEADD(DAY, -30, GETDATE());
    """

    rows, _ = execute_query(query, fetch=True)

    headers = ["transaction_id", "transaction_date", "final_amount"]

    print("Last 30 days transaction:")
    for row in rows:
        row_dict = dict(zip(headers, row))
        print(row_dict)
    
    upload_query_results_to_s3(
        "analytics/last_30_days_transaction.csv",
        rows,
        headers
    )
   

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
    headers = ["customer_id", "total_spent", "spending_rank"]

    print("Customers rank by total spending:")
    for row in rows:
        row_dict = dict(zip(headers, row))
        print(row_dict)
     
    upload_query_results_to_s3(
        "analytics/rank.csv",
        rows,
        headers
    )
    

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
    headers = ["region", "total_revenue"]

    print("Top Region:", dict(zip(headers, rows)))

    upload_query_results_to_s3(
        "analytics/top_performing_region.csv",
        rows,
        headers
    )

if __name__ == "__main__":
    company_summary_metrics()
    high_performing_regions()
    last_30_days_transactions()
    rank_customers_by_spending()
    top_performing_region()