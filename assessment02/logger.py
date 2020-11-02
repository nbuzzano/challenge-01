import json
import inspect

class Logger:
	#static vars
	config_file = ''
	env_file = ''
	current_env = 'dev'#should get from OS env !!!

	#instance vars
	current_config_item = None
	log_relevance = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
	
	
	@staticmethod
	def set_configs(config_file, env_file):
		Logger.config_file = config_file
		Logger.check_file_format()
		Logger.env_file = env_file
		Logger.check_env_format()


	@staticmethod
	def check_env_format():
		env_mandatory_keys = ['dev', 'stage', 'production']
		
		with open(Logger.env_file) as env_file:
			env_items = json.load(env_file)

			#checking if all env_mandatory_keys are present
			for env_key in env_mandatory_keys:
				if env_key not in env_items:
					raise KeyError(env_key + " is not a key value found in env file")


	@staticmethod
	def check_file_format():
		
		mandatory_file_keys = ['level', 'filename']
		
		with open(Logger.config_file) as config_file:
			config_items = json.load(config_file)
			
			for config_key in config_items.keys():
				config_item = config_items[config_key]

				#checking if level key has a valid value
				if config_item['level'] not in Logger.log_relevance:
					raise KeyError(config_item['level'] + ' is not a log relevance valid value')

				#checking if all mandatory_file_keys are present
				for mandatory_k in mandatory_file_keys:
					if mandatory_k not in config_item:
						raise KeyError("No " + mandatory_k + " key value found in " + config_key + " file")


	@staticmethod
	def get_logger(logger_name):
		with open(Logger.config_file) as config_file:
			config_items = json.load(config_file)
			config_item = config_items[logger_name]

			logger = Logger()
			logger.current_config_item = config_item
			return logger


	def log(self, log_text):

		if self.should_log():
			
			level = self.current_config_item['level']
			level_tag = self.build_tag(level)

			calling_file = inspect.stack()[1][1] #getting caller file
			calling_function = inspect.stack()[1][3] #getting caller function
			file_tag, function_tag = self.build_tag(calling_file), self.build_tag(calling_function)
			
			log_msg = level_tag + file_tag + function_tag + log_text
			print(log_msg)
			# Also write logs to an output file

	
	def should_log(self):
		logger_level = self.current_config_item['level']
		current_env_key = Logger.current_env

		current_env_value = None
		with open(Logger.env_file) as env_file:
			env_items = json.load(env_file)
			current_env_value = env_items[current_env_key]

		relevance_list = []
		for relevance_item in reversed(Logger.log_relevance):
			relevance_list.append(relevance_item)
			if relevance_item == current_env_value:
				break

		return logger_level in relevance_list 
		
	
	def build_tag(self, tag):
		return '[' + tag + '] '


def test():
	Logger.set_configs('log_config.txt', 'logging_levels.txt')
	test_logger = Logger.get_logger('info_logger')
	test_logger.log('log certain event')

test()

