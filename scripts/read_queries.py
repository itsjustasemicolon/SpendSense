import pandas as pd
from sqlalchemy import create_engine, text
import traceback

def read_query(query_name):
    with open("scripts/queries.sql", 'r') as file:
        content = file.read()

    queries = [q.strip() for q in content.split('--@name:')]
    for q in queries:
        lines = q.split('\n', 1)
        name = lines[0].strip()
        query = lines[1].strip() if len(lines) > 1 else ''
        if name == query_name:
            return query

    raise ValueError(f"Query with name '{query_name}' not found in the file.")

def query(query_name, **kwargs):
    connection_uri = "postgresql://postgres:password@postgres:5432/personal_finance_dashboard"
    sql = read_query(query_name)
    db_engine = create_engine(connection_uri)
    
    try:
        # Special handling for credit card summary query
        if query_name == "credit_card_summary":
            try:
                # Convert SQL query to text object and explicitly set column names
                sql_text = text(sql)
                with db_engine.connect() as conn:
                    result = conn.execute(sql_text)
                    # Manually construct DataFrame from result
                    columns = result.keys()
                    data = [dict(zip(columns, row)) for row in result.fetchall()]
                    df = pd.DataFrame(data)
                    
                    # Ensure numeric columns have correct types
                    if 'spent' in df.columns:
                        df['spent'] = pd.to_numeric(df['spent'], errors='coerce').fillna(0.0)
                    if 'limit' in df.columns:
                        df['limit'] = pd.to_numeric(df['limit'], errors='coerce').fillna(1500.0)
                    
                    df.index = range(1, len(df) + 1)
                    return df
            except Exception as e:
                print(f"Error in credit_card_summary: {str(e)}")
                print(traceback.format_exc())
                # Return empty DataFrame with expected columns
                return pd.DataFrame(columns=['card_name', 'spent', 'limit'])
        
        # Regular query handling for other queries
        if kwargs:
            with db_engine.connect() as conn:
                df = pd.read_sql(text(sql), conn, params=kwargs)
        else:
            df = pd.read_sql(sql, db_engine)
        
        df.index = range(1, len(df) + 1)
        return df
    except Exception as e:
        print(f"Error executing query '{query_name}': {str(e)}")
        print(traceback.format_exc())
        
        # Return appropriate fallback based on query type
        if query_name == "credit_card_summary":
            return pd.DataFrame(columns=['card_name', 'spent', 'limit'])
        
        # For other queries, re-raise the exception
        raise
