from langchain_core.tools import tool

@tool
def query_dummy_database(query: str) -> str:
    """
    Executes a SQL query against the 'sales_db' database.
    Use this tool whenever you need to answer questions about revenue, sales, or users.
    
    Args:
        query: The SQL query to execute (e.g., "SELECT * FROM sales")
    """
    print(f"🛠️ Tool executing SQL: {query}")
    
    # Normalize the query to handle case sensitivity (make everything UPPERCASE)
    q_upper = query.upper()
    
    # Check for keywords regardless of exact syntax
    # We accept 'REVENUE' or 'AMOUNT' because the LLM might guess either
    if "SELECT" in q_upper and "SUM" in q_upper and ("AMOUNT" in q_upper or "REVENUE" in q_upper):
        return "[{'total_revenue': 50240.00}]"
    
    if "COUNT" in q_upper and "FROM SALES" in q_upper:
        return "[{'user_count': 1250}]"
        
    return "[{'error': 'Table not found or Query not understood. Try querying the sales table for 'amount'.'}]"
