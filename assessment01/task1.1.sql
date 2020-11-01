/*1.1​ ​Write a SQL query to get a list of accounts and include the:
- total historical MRR,
- total historical usage revenue, 
- and total historical paid (orders with payment status “success”). 

*/


SELECT 	acc.id, 	
		sum(mrr.amount_exc_tax) as mrr, 
		sum(r_usage.amount_exc_tax) as usage,
		sum(orders.amount_exc_tax) as paid
FROM accounts acc 
JOIN revenue_mrr mrr ON mrr.account_id = acc.id 
JOIN revenue_usage r_usage ON r_usage.account_id = acc.id
JOIN (
	SELECT account_id, amount_exc_tax
	FROM orders
	WHERE status = 'success' 
) orders ON orders.account_id = acc.id
GROUP BY acc.id
ORDER BY acc.id;