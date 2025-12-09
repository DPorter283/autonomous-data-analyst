from langchain_core.tools import tool

@tool
def query_dummy_database(query: str) -> str:
    """
    Executes a SQL query against the 'sales_db' database.
    Use this tool whenever you need to answer questions about revenue, sales, or users.
    
    Args:
        query: The SQL query to execute (e.g., "SELECT * FROM sales")
    """
    # 1. Log what the agent is trying to do (Debugging)
    print(f"🛠️ Tool executing SQL: {query}")
    
    # 2. Simulate a database response (We will replace this with Redshift later)
    # This is a "Mock" - a standard senior engineering practice for testing.
    if "SELECT sum(amount)" in query.upper():
        return "[{'total_revenue': 50240.00}]"
    
    if "COUNT(*)" in query.upper():
        return "[{'user_count': 1250}]"
        
    return "[{'error': 'Table not found. Try querying the 'sales' table.'}]"