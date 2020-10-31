

--DROP TABLE IF EXISTS accounts;
DROP TABLE accounts CASCADE;
CREATE TABLE accounts (id SERIAL PRIMARY KEY, plan varchar, country varchar);
-- should use a relative path like ~/sirena-assessment/assessment01/accounts.csv
COPY accounts FROM '/Users/nicolasbuzzano/Documents/github/sirena-assessment/assessment01/accounts.csv' CSV HEADER;

/* ========+========+========+========+========+========+========+ */

DROP TABLE IF EXISTS revenue_mrr;
CREATE TABLE revenue_mrr (
	id SERIAL PRIMARY KEY, account_id smallint, amount_exc_tax real, amount_incl_tax real, created_at date,
	CONSTRAINT fk_accounts
      	FOREIGN KEY(account_id) 
	  	REFERENCES accounts(id)
	  	ON DELETE SET NULL
	);
-- should use a relative path like ~/sirena-assessment/assessment01/accounts.csv
COPY revenue_mrr FROM '/Users/nicolasbuzzano/Documents/github/sirena-assessment/assessment01/revenue_mrr.csv' CSV HEADER;

/* ========+========+========+========+========+========+========+ */

DROP TABLE IF EXISTS revenue_usage;
CREATE TABLE revenue_usage (
	id SERIAL PRIMARY KEY, account_id smallint, amount_exc_tax real, amount_incl_tax real, created_at date,
	CONSTRAINT fk_accounts
      	FOREIGN KEY(account_id) 
	  	REFERENCES accounts(id)
	  	ON DELETE SET NULL
	);
-- should use a relative path like ~/sirena-assessment/assessment01/accounts.csv
COPY revenue_usage FROM '/Users/nicolasbuzzano/Documents/github/sirena-assessment/assessment01/revenue_usage.csv' CSV HEADER;

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
-- should use a relative path like ~/sirena-assessment/assessment01/accounts.csv
COPY orders FROM '/Users/nicolasbuzzano/Documents/github/sirena-assessment/assessment01/orders.csv' CSV HEADER;

/* ========+========+========+========+========+========+========+ */

