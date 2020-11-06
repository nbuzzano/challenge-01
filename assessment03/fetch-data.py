from covid_api import CovidAPI
import pandas as pd

def fetch():
	c = CovidAPI.get_countries()
	df = pd.read_json(c)
	df.to_csv()


fetch()