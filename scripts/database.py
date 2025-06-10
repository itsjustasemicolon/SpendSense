import pandas as pd
from sqlalchemy import create_engine, text

def extract(file):
    raw_transactions = pd.read_csv(file)
    return raw_transactions

def transform(df):
    col_names = ['Type', 'Date', 'Title', 'Amount', 'Currency', 'Category', 'Account', 'Status']
    cleaned_df = df.loc[df['Status'] == 'Reconciled', col_names]
    new_col_names = ['type', 'date', 'item', 'amount', 'currency', 'category', 'account', 'status']
    cleaned_df.columns = new_col_names
    cleaned_df['date'] = pd.to_datetime(cleaned_df['date'])
    # Normalize type values for easier querying
    cleaned_df['type'] = cleaned_df['type'].str.lower().str.strip()
    # Ensure amount is numeric
    cleaned_df['amount'] = pd.to_numeric(cleaned_df['amount'], errors='coerce').fillna(0)
    return cleaned_df

def load(df, db_table, connection_uri):
    db_engine = create_engine(connection_uri)
    df.to_sql(
        name=db_table,
        con=db_engine,
        if_exists="replace",
        index=False)

def drop(table, connection_uri):
    db_engine = create_engine(connection_uri)
    with db_engine.connect() as connection:
        connection.execute(text(f"DROP TABLE IF EXISTS {table};"))
        connection.commit()

# --- NEW: Helper functions for queries ---

def get_monthly_cash_flow(connection_uri):
    db_engine = create_engine(connection_uri)
    query = """
        SELECT
            DATE_TRUNC('month', date) AS month,
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) -
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS cash_flow
        FROM transactions
        GROUP BY month
        ORDER BY month
    """
    with db_engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def get_transactions_by_date(connection_uri, date):
    db_engine = create_engine(connection_uri)
    query = text("""
        SELECT *
        FROM transactions
        WHERE DATE(date) = :date
        ORDER BY date
    """)
    with db_engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"date": date})
    return df