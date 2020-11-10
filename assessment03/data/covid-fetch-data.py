from covid_api import CovidAPI, APIHelper
from datetime import datetime
import pandas as pd
import numpy as np
import csv

def fetch_all():
	print('fetching countries_and_continents...')
	#fetch_countries_and_continents()
	print('fetching countries_and_continents DONE')
	print('')
	
	print('fetching covid_cases...')
	#fetch_covid_cases()
	print('fetching covid_cases DONE')
	print('')
	
	print('fetching covid_summaries...')
	fetch_covid_summaries()
	print('fetching covid_summaries DONE')
	print('')

	print('fetching owid_covid_data...')
	#fetch_owid_covid_data()
	print('fetching owid_covid_data DONE')
	print('')

	print('fetching fetch_covid_owid_csv...')
	#fetch_covid_owid_csv()
	print('fetching fetch_covid_owid_csv DONE')
	print('')
	


def fetch_countries_and_continents():
	url = 'https://pkgstore.datahub.io/JohnSnowLabs/country-and-continent-codes-list/country-and-continent-codes-list-csv_csv/data/b7876b7f496677669644f3d1069d3121/country-and-continent-codes-list-csv_csv.csv'
	data = pd.read_csv(url)
	data.to_csv('country-and-continent-codes-list-csv_csv.csv')

	df = pd.DataFrame(columns=['continent_code', 'country_code'])
	df['continent_code'] = data.Continent_Code
	df['country_code'] = data.Two_Letter_Country_Code
	df['continent_name'] = data.Continent_Name
	df['country_name'] = data.Country_Name
	
	df = df.sort_values('continent_code')
	df = df.dropna()

	df.to_csv('country-and-continent-codes-list-csv_csv.csv')


def fetch_covid_cases():

	def look_for(k, arr):
		for i in arr['locations']:
			if i['country_code'] == k:
				return i['history']

	continent_and_countries = pd.read_csv('country-and-continent-codes-list-csv_csv.csv')
	def look_for_continent(country_key):
		for i in range(0,len(continent_and_countries)):
			item = continent_and_countries.iloc[i]
			if item.country_code == country_key:
				return item.continent_code

	all_countries = CovidAPI.get_task('/all')
	deaths = all_countries['deaths']
	confirmed = all_countries['confirmed']
	recovered = all_countries['recovered']

	columns = ['country_code', 'date', 'deaths', 'confirmed', 'recovered', 'continent_code']
	df = pd.DataFrame(columns=columns)
	
	i=0
	for country_key, country_value in CovidAPI.get_countries().items():
		country_deaths = look_for(country_key, deaths)
		country_confirmed = look_for(country_key, confirmed)
		country_recovered = look_for(country_key, recovered)

		continent_code = look_for_continent(country_key)

		if country_deaths != None and country_confirmed != None and country_recovered != None:
			for date, death_amount in country_deaths.items():
				confirmed_amount = country_confirmed[date]
				recovered_amount = country_recovered[date]
				date = datetime.strptime(date, '%m/%d/%y')
				df.loc[i] = [country_key, date, death_amount, confirmed_amount, recovered_amount, continent_code]
				i=i+1

	df = df.sort_values(['country_code', 'date'])
	df.to_csv('covid_cases.csv')


def fetch_covid_summaries():

	def calculate_percentage(current_population, country_population):
		try:
			precision = 5
			return round((current_population*100.0)/country_population, precision)
		except:
			return None


	columns = ['country_name', 'country_code', 'deaths_percentage', 'confirmed_percentage', 'recovered_percentage', 'deaths', 'confirmed', 'recovered']
	df = pd.DataFrame(columns=columns)

	i=0
	payload = {'timelines': 'false'}
	response = CovidAPI.get_task('/v2/locations', payload=payload)

	for location in response["locations"]:
		country_population = location['country_population']
		country_code = location['country_code']
		country_name = location['country']
		latest = location["latest"]        

		confirmed = latest['confirmed']
		recovered = latest['recovered']
		deaths = latest['deaths']

		confirmed_percentage = calculate_percentage(confirmed, country_population)
		recovered_percentage = calculate_percentage(recovered, country_population)
		deaths_percentage = calculate_percentage(deaths, country_population)
		df.loc[i] = [country_name, country_code, deaths_percentage, confirmed_percentage, recovered_percentage, deaths, confirmed, recovered]
		i=i+1

	df.to_csv('covid_summaries.csv')


def fetch_owid_covid_data():
	url = 'https://covid.ourworldindata.org/data/owid-covid-data.json'
	owid_covid_data_dict = APIHelper.get(url)

	columns = [
	"country_code",
	"population",
	"population_density",
	"median_age",
	"aged_65_older",
	"aged_70_older",
	"gdp_per_capita",
	"cardiovasc_death_rate",
	"diabetes_prevalence",
	"handwashing_facilities",
	"hospital_beds_per_thousand",
	"life_expectancy",
	"female_smokers",
	"male_smokers",
	"extreme_poverty",
	"human_development_index"
	]

	coutries_codes_2_and_3 = pd.read_excel('Comtrade_Country_Code and_ISO_list.xlsx')

	def map_iso_code_3_to_2(iso_code_3):
		i=0
		for i in range(0,len(coutries_codes_2_and_3)):
			item = coutries_codes_2_and_3.iloc[i]
			i=i+1
			try:
				if item['ISO3-digit Alpha'] == iso_code_3:
					return item['ISO2-digit Alpha']
			except:
				continue

	df = pd.DataFrame(columns=columns)

	#create a df with just 'columns' items and also, iso 3 country code instead of iso 2.
	i=0
	for key_iso_code_3 in owid_covid_data_dict.keys():
		values = []
		iso_code_2 = map_iso_code_3_to_2(key_iso_code_3)
		values.append(iso_code_2)

		#looking in dict the features that we want. 
		country = owid_covid_data_dict[key_iso_code_3]
		for column_name in columns[1:]:
			try:
				values.append(country[column_name])
			except:
				values.append(None)

		df.loc[i] = values
		i=i+1

	
	df_summaries = pd.read_csv('covid_summaries.csv')
	df_owid_covid = pd.merge(df, df_summaries, on='country_code', how='inner')
	df_owid_covid.to_csv('owid-covid-data-summary.csv')

	del df_owid_covid['deaths_percentage']
	del df_owid_covid['confirmed_percentage']
	del df_owid_covid['recovered_percentage']

	for column_name in df_owid_covid.columns:
		if column_name != 'country_code':
			df_owid_covid[column_name] = pd.to_numeric(df_owid_covid[column_name])

	df_owid_covid.to_csv('owid_covid_data.csv')


def fetch_covid_owid_csv():
	filename = 'covid-data.csv'
	data_url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
	data_content = requests.get(data_url).content
	csv_file = open(filename, 'wb')
	csv_file.write(data_content)
	csv_file.close()


fetch_all()

