import pandas as pd
from sqlalchemy import create_engine, text

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
    # If the query needs parameters (like transactions_by_date)
    if kwargs:
        with db_engine.connect() as conn:
            df = pd.read_sql(text(sql), conn, params=kwargs)
    else:
        df = pd.read_sql(sql, db_engine)
    df.index = range(1, len(df) + 1)
    return df