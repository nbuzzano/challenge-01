import json
import inspect
import os

class Logger:
	#static vars
	config_file = ''
	env_file = ''
	current_env = os.environ['CURRENT_ENV']

	#instance vars
	current_config_item = None
	log_relevance = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
	
	
	@staticmethod
	def set_configs(config_file, env_file):
		Logger.config_file = config_file
		Logger.check_file_format()
		Logger.env_file = env_file
		Logger.check_env_format()

		#if everything is ok, create logger folder.
		Logger.create_logs_folder()


	@staticmethod
	def create_logs_folder():
			path = 'logs' + '/' + Logger.current_env 
			if not os.path.exists(path):
				try:
					os.makedirs(path)
				except OSError as e:
					if e.errno != errno.EEXIST:
						raise

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

			#creating a Logger instance and setting the according config.
			logger = Logger()
			logger.current_config_item = config_item
			return logger


	def log(self, log_text):

		if self.should_log():
			
			level = self.current_config_item['level']
			level_tag = self.build_tag(level)

			#getting some metadata to create the log message.
			calling_file = inspect.stack()[1][1] #getting caller file
			calling_function = inspect.stack()[1][3] #getting caller function
			file_tag, function_tag = self.build_tag(calling_file), self.build_tag(calling_function)
			
			#print and write to log file
			log_msg = level_tag + file_tag + function_tag + log_text
			print(log_msg)

			#writing down message on the current env folder.
			log_filename = self.current_config_item['filename']
			with open('logs/' + Logger.current_env + '/' + log_filename, 'a') as log_file:
				log_file.write(log_msg + '\n')

			return log_msg

	def should_log(self):
		"""
			Using the log_relevance list to check if the level of this instance
			is lower or higher than the level of the current enviroment.
			If is lower shouldn't log, if it's equal or higher it should.
		"""
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

