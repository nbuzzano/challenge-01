from covid_api import CovidAPI
import pandas as pd
import csv

def fetch():
	all_countries = CovidAPI.get_task('/all')
	deaths = all_countries['deaths']
	confirmed = all_countries['confirmed']
	recovered = all_countries['recovered']
	
	world_list = [] 
	for d,c,r in zip(deaths,confirmed,recovered):
		world_list.append((d,c,r))

	#df = pd.read_json(c)
	#df.to_csv()


#fetch()

def save(csv_file, csv_columns, dic_data):
	try:
		with open(csv_file, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			for data in dict_data:
				writer.writerow(data)
	except IOError:
		print("I/O error")


csv_columns = ['No','Name','Country','mi_dic']
dict_data = [{'No': 1, 'Name': 'Alex', 'Country': 'India', 'mi_dic': {'sub_k': 'sub_v'}}]
csv_file = "data/Names.csv"

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            print(type(data))
            writer.writerow(data)

except IOError:
    print("I/O error")

df = pd.read_csv(csv_file)
print(df.iloc[0]['mi_dic'])
print(type(df.iloc[0]['mi_dic']))