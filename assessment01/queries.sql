
/*1.1​ ​Write a SQL query to get a list of accounts and include the:
- total historical MRR,
- total historical usage revenue, 
- and total historical paid (orders with payment status “success”). 

Your result should look something like this:
*/

SELECT 	acc.id, 	
		sum(mrr.amount_exc_tax) as mrr_sum, 
		sum(r_usage.amount_exc_tax) as r_usage_sum
FROM accounts acc 
JOIN revenue_mrr mrr ON mrr.account_id = acc.id 
JOIN revenue_usage r_usage ON r_usage.account_id = acc.id 
GROUP BY acc.id;

SELECT 	acc.id, 	
		sum(orders.amount_exc_tax) as orders_sum
FROM accounts acc 
JOIN orders ON orders.account_id = acc.id
WHERE status = 'success' 
GROUP BY acc.id;
