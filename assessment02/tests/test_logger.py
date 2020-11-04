
import os

#env value should be set using pycharm for example.
os.environ['CURRENT_ENV'] = 'dev'

from sirena_utils.logger import Logger

#===========+===========+===========+===========+===========#

def test_logger_tool_warning():
	
	""" CURRENT_ENV == 'dev' and according to logging_levels 'dev' == INFO
		So its expected that using a logger with WARNING relevance an output should be made.
	"""

	config_path = 'config/'
	Logger.set_configs(config_path + 'log_config.json', config_path + 'logging_levels.json')
	test_logger = Logger.get_logger('warning_logger')
	log_msg = 'log certain event'
	output = test_logger.log(log_msg)

	calling_file = output.split()[1]
	assert output == '[WARNING] ' + calling_file + ' [test_logger_tool_warning] ' + log_msg


test_logger_tool_warning()

#===========+===========+===========+===========+===========#

def test_logger_tool_debug():
	
	""" CURRENT_ENV == 'dev' and according to logging_levels 'dev' == INFO
		So since this is a logger with DEBUG relevance (lower than INFO) we wont log any message.
	"""
	
	config_path = 'config/'
	Logger.set_configs(config_path + 'log_config.json', config_path + 'logging_levels.json')
	test_logger = Logger.get_logger('debug_logger')
	log_msg = 'log certain event'
	output = test_logger.log(log_msg)
	assert output == None


test_logger_tool_debug()

#===========+===========+===========+===========+===========#

def test_logger_tool_info():
	
	""" CURRENT_ENV == 'dev' and according to logging_levels 'dev' == INFO
		So its expected that using a logger with INFO relevance an output should be made.
	"""

	config_path = 'config/'
	Logger.set_configs(config_path + 'log_config.json', config_path + 'logging_levels.json')
	test_logger = Logger.get_logger('info_logger')
	log_msg = 'log certain event'
	output = test_logger.log(log_msg)

	calling_file = output.split()[1]
	assert output == '[INFO] ' + calling_file + ' [test_logger_tool_info] ' + log_msg


test_logger_tool_info()

