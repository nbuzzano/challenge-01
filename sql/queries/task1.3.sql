
/*1.3​ Write a SQL query to get accounts that have churned (accounts that stopped having a 
- revenune_mrr at some point in time) with their churn date and last MRR.

*/

SELECT acc.id, churn_date_table.created_at, last_mrr_table.amount_exc_tax
FROM accounts acc
JOIN (
	SELECT account_id, created_at FROM 
	(
	    SELECT *, ROW_NUMBER() 
	    OVER (PARTITION BY orders.account_id order by created_at DESC) AS Row_ID FROM orders
	) AS A
	WHERE Row_ID = 1
) churn_date_table ON churn_date_table.account_id = acc.id

JOIN (
	SELECT account_id, amount_exc_tax FROM 
	(
	    SELECT *, ROW_NUMBER() 
	    OVER (PARTITION BY revenue_mrr.account_id order by created_at DESC) AS Row_ID FROM revenue_mrr
	) AS A
	WHERE Row_ID = 1
) last_mrr_table ON last_mrr_table.account_id = acc.id

WHERE acc.id NOT IN --NOT
	(SELECT acc.id
		FROM accounts acc
		JOIN orders ON acc.id = orders.account_id
		WHERE (extract(month FROM orders.created_at) = extract(month FROM CURRENT_DATE) AND 
				extract(year FROM orders.created_at) = extract(year FROM CURRENT_DATE))
		GROUP BY acc.id)

GROUP BY acc.id, churn_date_table.created_at, last_mrr_table.amount_exc_tax
ORDER BY acc.id;

