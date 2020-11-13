import json
import inspect
import os

class Logger:
	
	#static vars
	__config_file = ''
	__env_file = ''
	__current_env = os.environ['CURRENT_ENV']
	__log_relevance = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
	
	
	def __init__(self, current_config_item):
		self.current_config_item = current_config_item
	
	
	@staticmethod
	def set_configs(config_file, env_file):
		#checking if files have valid formats and values.
		Logger.__config_file = config_file
		Logger.__check_file_format()
		Logger.__env_file = env_file
		Logger.__check_env_format()

		#if everything is ok, create logger folder.
		Logger.__create_logs_folder()


	@staticmethod
	def __create_logs_folder():
		#creating logs folder if its not created yet.	
		path = 'logs' + '/' + Logger.__current_env 
		if not os.path.exists(path):
			try:
				os.makedirs(path)
			except OSError as e:
				if e.errno != errno.EEXIST:
					raise

	@staticmethod
	def __check_env_format():
		env_mandatory_keys = ['dev', 'stage', 'production']
		
		with open(Logger.__env_file) as env_file:
			env_items = json.load(env_file)

			#checking if all env_mandatory_keys are present
			for env_key in env_mandatory_keys:
				if env_key not in env_items:
					raise KeyError(env_key + " is not a key value found in env file")


	@staticmethod
	def __check_file_format():
		
		mandatory_file_keys = ['level', 'filename']
		
		with open(Logger.__config_file) as config_file:
			config_items = json.load(config_file)
			
			for config_key in config_items.keys():
				config_item = config_items[config_key]

				#checking if level key has a valid value
				if config_item['level'] not in Logger.__log_relevance:
					raise KeyError(config_item['level'] + ' is not a log relevance valid value')

				#checking if all mandatory_file_keys are present
				for mandatory_k in mandatory_file_keys:
					if mandatory_k not in config_item:
						raise KeyError("No " + mandatory_k + " key value found in " + config_key + " file")


	@staticmethod
	def get_logger(logger_name):
		with open(Logger.__config_file) as config_file:
			config_items = json.load(config_file)
			config_item = config_items[logger_name]

			#creating a Logger instance and setting the according config.
			logger = Logger(config_item)
			return logger


	def log(self, log_text):

		if self.__should_log():
			
			level = self.current_config_item['level']
			level_tag = self.__build_tag(level)

			#getting some metadata to create the log message.
			calling_file = inspect.stack()[1][1] #getting caller file
			calling_function = inspect.stack()[1][3] #getting caller function
			file_tag, function_tag = self.__build_tag(calling_file), self.__build_tag(calling_function)
			
			#print and write to log file
			log_msg = level_tag + file_tag + function_tag + log_text
			print(log_msg)

			#writing down message on the current env folder.
			log_filename = self.current_config_item['filename']
			with open('logs/' + Logger.__current_env + '/' + log_filename, 'a') as log_file:
				log_file.write(log_msg + '\n')

			return log_msg


	def __should_log(self):
		"""
			Using the log_relevance list to check if the level of this instance
			is lower or higher than the level of the current enviroment.
			If is lower shouldn't log, if it's equal or higher it should.
		"""
		logger_level = self.current_config_item['level']
		current_env_key = Logger.__current_env

		current_env_value = None
		with open(Logger.__env_file) as env_file:
			env_items = json.load(env_file)
			current_env_value = env_items[current_env_key]

		relevance_list = []
		for relevance_item in reversed(Logger.__log_relevance):
			relevance_list.append(relevance_item)
			if relevance_item == current_env_value:
				break

		return logger_level in relevance_list 
		
	
	def __build_tag(self, text_tag):
		return '[' + text_tag + '] '

