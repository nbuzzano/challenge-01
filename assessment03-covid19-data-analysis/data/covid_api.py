import requests

class ApiError(Exception):
	pass


class APIHelper:
	
	@staticmethod
	def get(url):
		print('fetching ' + url)
		resp = requests.get(url)
		if resp.status_code != 200:
		    raise ApiError('GET ' + url + '/ {}'.format(resp.status_code))

		return resp.json()


class CovidAPI:

	__base_url = 'https://covid-tracker-us.herokuapp.com'

	@staticmethod
	def __build_url(task):
		return CovidAPI.__base_url + task
	
	
	@staticmethod
	def get_task(task_path, payload=None):

		base_url = CovidAPI.__build_url(task_path)
		payload = CovidAPI.__build_payload(payload)
		final_path = base_url + payload
		
		resp = APIHelper.get(final_path)
		return resp

	@staticmethod
	def __build_payload(params=None):
		payload = ''
		if params is not None:
			payload = '?'
		
			for k, v in params.items():
				payload = payload + (k + '=' + v + '&')
			payload = payload[:-1] #removing last '&'

		return payload

	
	@staticmethod
	def get_countries():
		return APIHelper.get('http://country.io/names.json')


def fetch_v1():
	# API v1 
	CovidAPI.get_task('/confirmed')
	CovidAPI.get_task('/recovered')
	CovidAPI.get_task('/deaths')


def fetch_v2():
	# API v2
	CovidAPI.get_task('/v2/sources')
	CovidAPI.get_task('/v2/latest')
	
	payload = {'country_code': 'AR', 'timelines': 'false'}
	CovidAPI.get_task('/v2/locations', payload=payload)
	

def test():
	fetch_v1()
	fetch_v2()


#test()




