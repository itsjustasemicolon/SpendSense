--@name: raw_transactions
SELECT * FROM raw_transactions;

--@name: transactions
SELECT * FROM transactions;

--@name: monthly_amount_over_time
SELECT
    month,
    SUM(amount) OVER (ORDER BY month) AS net_worth,
    SUM(CASE WHEN account = 'Wallet' THEN amount ELSE 0 END) OVER (ORDER BY month) AS wallet,
    SUM(CASE WHEN account = 'Union Bank' THEN amount ELSE 0 END) OVER (ORDER BY month) AS unionbank,
    SUM(CASE WHEN account = 'Seabank' THEN amount ELSE 0 END) OVER (ORDER BY month) AS seabank,
    SUM(CASE WHEN account = 'GCash' THEN amount ELSE 0 END) OVER (ORDER BY month) AS gcash,
    SUM(CASE WHEN account = 'Maya' THEN amount ELSE 0 END) OVER (ORDER BY month) AS maya,
    SUM(CASE WHEN account = 'GrabPay' THEN amount ELSE 0 END) OVER (ORDER BY month) AS grabpay,
    SUM(CASE WHEN account = 'ShopeePay' THEN amount ELSE 0 END) OVER (ORDER BY month) AS shopeepay,
    SUM(CASE WHEN account = 'Binance' THEN amount ELSE 0 END) OVER (ORDER BY month) AS binance,
    SUM(CASE WHEN account = 'Ronin' THEN amount ELSE 0 END) OVER (ORDER BY month) AS ronin
FROM
    (SELECT
		DATE_TRUNC('month', date) AS month,
		account,
		SUM(ROUND(amount)) AS amount
	FROM
		transactions
	GROUP BY 
		month, account
	ORDER BY
		month);

--@name: weekly_amount_over_time
SELECT
    week,
    SUM(amount) OVER (ORDER BY week) AS net_worth,
    SUM(CASE WHEN account = 'Wallet' THEN amount ELSE 0 END) OVER (ORDER BY week) AS wallet,
    SUM(CASE WHEN account = 'Union Bank' THEN amount ELSE 0 END) OVER (ORDER BY week) AS unionbank,
    SUM(CASE WHEN account = 'Seabank' THEN amount ELSE 0 END) OVER (ORDER BY week) AS seabank,
    SUM(CASE WHEN account = 'GCash' THEN amount ELSE 0 END) OVER (ORDER BY week) AS gcash,
    SUM(CASE WHEN account = 'Maya' THEN amount ELSE 0 END) OVER (ORDER BY week) AS maya,
    SUM(CASE WHEN account = 'GrabPay' THEN amount ELSE 0 END) OVER (ORDER BY week) AS grabpay,
    SUM(CASE WHEN account = 'ShopeePay' THEN amount ELSE 0 END) OVER (ORDER BY week) AS shopeepay,
    SUM(CASE WHEN account = 'Binance' THEN amount ELSE 0 END) OVER (ORDER BY week) AS binance,
    SUM(CASE WHEN account = 'Ronin' THEN amount ELSE 0 END) OVER (ORDER BY week) AS ronin
FROM
    (SELECT
		DATE_TRUNC('week', date) + INTERVAL '6 days' AS week,
		account,
		SUM(ROUND(amount)) AS amount
	FROM
		transactions
	GROUP BY 
		week, account
	ORDER BY
		week);

--@name: daily_amount_over_time
SELECT
    day,
    SUM(amount) OVER (ORDER BY day) AS net_worth,
    SUM(CASE WHEN account = 'Wallet' THEN amount ELSE 0 END) OVER (ORDER BY day) AS wallet,
    SUM(CASE WHEN account = 'Union Bank' THEN amount ELSE 0 END) OVER (ORDER BY day) AS unionbank,
    SUM(CASE WHEN account = 'Seabank' THEN amount ELSE 0 END) OVER (ORDER BY day) AS seabank,
    SUM(CASE WHEN account = 'GCash' THEN amount ELSE 0 END) OVER (ORDER BY day) AS gcash,
    SUM(CASE WHEN account = 'Maya' THEN amount ELSE 0 END) OVER (ORDER BY day) AS maya,
    SUM(CASE WHEN account = 'GrabPay' THEN amount ELSE 0 END) OVER (ORDER BY day) AS grabpay,
    SUM(CASE WHEN account = 'ShopeePay' THEN amount ELSE 0 END) OVER (ORDER BY day) AS shopeepay,
    SUM(CASE WHEN account = 'Binance' THEN amount ELSE 0 END) OVER (ORDER BY day) AS binance,
    SUM(CASE WHEN account = 'Ronin' THEN amount ELSE 0 END) OVER (ORDER BY day) AS ronin
FROM
    (SELECT
		DATE(date) AS day,
		account,
		SUM(ROUND(amount)) AS amount
	FROM
		transactions
	GROUP BY 
		day, account
	ORDER BY
		day);

--@name: expenses_per_category
SELECT
    category,
    ROUND(ABS(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END))) as expenses
FROM
    transactions
GROUP BY
    category
HAVING
    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) <> 0
ORDER BY
	expenses DESC;

--@name: income_per_category
SELECT
    category,
    ROUND(ABS(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END))) as income
FROM
    transactions
GROUP BY
    category
HAVING
    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) <> 0
ORDER BY
	income DESC;

--@name: monthly_expenses
SELECT
    TO_CHAR(DATE_TRUNC('month', date), 'FMMonth YYYY') AS month,
    ABS(ROUND(SUM(amount))) AS expenses
FROM 
    transactions
WHERE
    type = 'expense'
GROUP BY
    DATE_TRUNC('month', date)
ORDER BY
    DATE_TRUNC('month', date);

--@name: monthly_income
SELECT
	TO_CHAR(DATE_TRUNC('month', date), 'FMMonth YYYY') AS month,
	ROUND(SUM(amount)) AS income
FROM
	transactions
WHERE
	type = 'income'
GROUP BY
	DATE_TRUNC('month', date)
ORDER BY 
	DATE_TRUNC('month', date);

--@name: weekly_expenses
SELECT
    DATE_TRUNC('week', date) + INTERVAL '6 days' AS week,
    ROUND(ABS(SUM(amount))) AS expenses
FROM
    transactions
WHERE
    type = 'expense'
GROUP BY
    DATE_TRUNC('week', date)
ORDER BY
    DATE_TRUNC('week', date);
	
--@name: daily_expenses
SELECT
    DATE(date) AS day,
	ROUND(ABS(SUM(amount))) as expenses
FROM
	transactions
WHERE
	type = 'expense'
GROUP BY
	day
ORDER BY
	day;
	
--@name: payment_methods
SELECT
	account,
	ROUND(ABS(SUM(amount))) as amount
FROM
	transactions
WHERE
	type = 'expense'
GROUP BY
	account
ORDER BY
	amount DESC;
	
--@name: receiving_methods
SELECT
	account,
	ROUND(ABS(SUM(amount))) as amount
FROM
	transactions
WHERE
	type = 'income'
GROUP BY
	account
ORDER BY
	amount DESC;

--@name: monthly_cash_flow
SELECT
    TO_CHAR(DATE_TRUNC('month', date), 'FMMonth YYYY') AS month,
    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) -
    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS cash_flow
FROM
    transactions
GROUP BY
    DATE_TRUNC('month', date)
ORDER BY
    DATE_TRUNC('month', date);

--@name: transactions_by_date
SELECT *
FROM transactions
WHERE DATE(date) = :date
ORDER BY date;

--@name: daily_net_summary_last_n_days
SELECT date,
       COALESCE(SUM(amount), 0) AS net_amount
FROM transactions
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY date
ORDER BY date;

--@name: credit_card_summary
SELECT 
    account AS card_name,
    CAST(COALESCE(SUM(CASE WHEN type = 'expense' THEN ABS(amount) ELSE 0 END), 0) AS FLOAT) AS spent,
    CAST(1500 AS FLOAT) AS "limit"
FROM transactions
WHERE (lower(account) LIKE '%credit%' 
       OR lower(account) LIKE '%visa%'
       OR lower(account) LIKE '%mastercard%'
       OR lower(account) LIKE '%amex%'
       OR lower(account) LIKE '%american express%'
       OR lower(account) LIKE '%discover%')
  AND date >= date_trunc('month', CURRENT_DATE)
GROUP BY account;
