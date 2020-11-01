

--DROP TABLE IF EXISTS accounts;
DROP TABLE accounts CASCADE;
CREATE TABLE accounts (id SERIAL PRIMARY KEY, plan varchar, country varchar);
\COPY accounts FROM 'data/accounts.csv' CSV HEADER;

/* ========+========+========+========+========+========+========+ */

DROP TABLE IF EXISTS revenue_mrr;
CREATE TABLE revenue_mrr (
	id SERIAL PRIMARY KEY, account_id smallint, amount_exc_tax real, amount_incl_tax real, created_at date,
	CONSTRAINT fk_accounts
      	FOREIGN KEY(account_id) 
	  	REFERENCES accounts(id)
	  	ON DELETE SET NULL
	);
\COPY revenue_mrr FROM 'data/revenue_mrr.csv' CSV HEADER;

/* ========+========+========+========+========+========+========+ */

DROP TABLE IF EXISTS revenue_usage;
CREATE TABLE revenue_usage (
	id SERIAL PRIMARY KEY, account_id smallint, amount_exc_tax real, amount_incl_tax real, created_at date,
	CONSTRAINT fk_accounts
      	FOREIGN KEY(account_id) 
	  	REFERENCES accounts(id)
	  	ON DELETE SET NULL
	);
\COPY revenue_usage FROM 'data/revenue_usage.csv' CSV HEADER;

/* ========+========+========+========+========+========+========+ */

CREATE TYPE status_type AS ENUM ('success', 'fail');
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
	id SERIAL PRIMARY KEY, account_id smallint, amount_exc_tax real, amount_incl_tax real, created_at date, status status_type,
	CONSTRAINT fk_accounts
      	FOREIGN KEY(account_id) 
	  	REFERENCES accounts(id)
	  	ON DELETE SET NULL
	);
\COPY orders FROM 'data/orders.csv' CSV HEADER;

/* ========+========+========+========+========+========+========+ */

