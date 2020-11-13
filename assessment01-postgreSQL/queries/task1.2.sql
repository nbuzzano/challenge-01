
/*
- 1.2​ ​Write a SQL query to get the monthly revenue (MRR and usage) coming from each plan.
*/

-- OPTION 1
SELECT 	acc.plan,
		extract(year FROM mrr.created_at) AS year, 
		extract(month FROM mrr.created_at) AS month,
		sum(mrr.amount_exc_tax) AS mrr_sum,
		sum(r_usage.amount_exc_tax) AS r_usage_sum
FROM accounts acc
JOIN revenue_mrr mrr ON mrr.account_id = acc.id 
JOIN revenue_usage r_usage ON r_usage.account_id = acc.id
GROUP BY acc.plan, extract(year FROM mrr.created_at), extract(month FROM mrr.created_at);


-- OPTION 2
SELECT 	extract(year FROM r_usage.created_at) AS year, 
		extract(month FROM r_usage.created_at) AS month,
		acc.plan AS plan,
		sum(r_usage.amount_exc_tax) AS amount,
		'usage' AS revenue_type
FROM accounts acc
JOIN revenue_usage r_usage ON r_usage.account_id = acc.id
GROUP BY acc.plan, extract(year FROM r_usage.created_at), extract(month FROM r_usage.created_at)
UNION
	SELECT 	extract(year FROM mrr.created_at) AS year, 
			extract(month FROM mrr.created_at) AS month,
			acc.plan,
			sum(mrr.amount_exc_tax) AS amount,
			'mrr' AS revenue_type
	FROM accounts acc
	JOIN revenue_mrr mrr ON mrr.account_id = acc.id 
	GROUP BY acc.plan, extract(year FROM mrr.created_at), extract(month FROM mrr.created_at)
ORDER BY year, month, plan, revenue_type;
