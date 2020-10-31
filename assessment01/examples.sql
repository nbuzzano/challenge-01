select acc.id, sum(mrr.amount_exc_tax)
	from accounts as acc
	join revenue_mrr as mrr
	on acc.id=mrr.account_id
	group by acc.id;


select sum(mrr.amount_exc_tax), acc.plan
	from accounts as acc
	join revenue_mrr as mrr
	on acc.id=mrr.account_id
	group by acc.plan;