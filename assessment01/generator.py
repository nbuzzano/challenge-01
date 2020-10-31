
from datetime import datetime, timedelta
import random
import time
import pandas as pd

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y', prop)


acc_ids = []
def get_arr_combinations(arr1, arr2):
	combinations = []
	acc_id = 0
	for i1 in arr1:
		for i2 in arr2:
			combinations.append((i1,i2))
			acc_ids.append(acc_id)
			acc_id = acc_id + 1

	return combinations


plans = ['PRO','BASIC']
countries = ['Argentina', 'Chile', 'Brazil']
revenue_types = ['mrr','usage','',]

#print(random.choice(['c','d','a','b','e','f','g']))

#amount_exc_tax -> excluded?
#amount_incl_tax -> included?

#=======#=======#=======#=======#=======#=======#=======#=======#=======#=======#

def generate_accounts():
	return get_arr_combinations(plans, countries)

i=0
df = pd.DataFrame(columns=['plan', 'country'])

for p,c in generate_accounts():
	df.loc[i] = [p,c]
	i=i+1

df.to_csv('accounts.csv', index=True)

#=======#=======#=======#=======#=======#=======#=======#=======#=======#=======#

def revenue_mrr():
	tax = 0.95
	amount_incl_tax = random.uniform(1000, 1200)
	amount_exc_tax = amount_incl_tax * tax

	n = 60
	today = datetime.today().strftime('%m/%d/%Y')
	date_N_days_ago = datetime.now() - timedelta(days=n)
	date_N_days_ago = date_N_days_ago.strftime('%m/%d/%Y')
	created_at = random_date(date_N_days_ago, today, random.random())

	account_id = random.choice(acc_ids)
	
	return account_id, amount_exc_tax, amount_incl_tax, created_at

df = pd.DataFrame(columns=['account_id', 'amount_exc_tax', 'amount_incl_tax', 'created_at'])

for i in range(0,100): 
	account_id, amount_exc_tax, amount_incl_tax, created_at = revenue_mrr()
	df.loc[i] = [account_id, amount_exc_tax, amount_incl_tax, created_at]

df.to_csv('revenue_mrr.csv', index=True)

#=======#=======#=======#=======#=======#=======#=======#=======#=======#=======#

def revenue_usage():
	return revenue_mrr()

df = pd.DataFrame(columns=['account_id', 'amount_exc_tax', 'amount_incl_tax', 'created_at'])

for i in range(0,100): 
	account_id, amount_exc_tax, amount_incl_tax, created_at = revenue_usage()
	df.loc[i] = [account_id, amount_exc_tax, amount_incl_tax, created_at]

df.to_csv('revenue_usage.csv', index=True)

#=======#=======#=======#=======#=======#=======#=======#=======#=======#=======#

statuses = ['success','fail']

def get_orders():

	return revenue_mrr()

df = pd.DataFrame(columns=['account_id', 'amount_exc_tax', 'amount_incl_tax', 'created_at', 'status'])

for i in range(0,100): 
	account_id, amount_exc_tax, amount_incl_tax, created_at = get_orders()
	status = random.choice(statuses)
	df.loc[i] = [account_id, amount_exc_tax, amount_incl_tax, created_at, status]

df.to_csv('orders.csv', index=True)



#=======#=======#=======#=======#=======#=======#=======#=======#=======#=======#



