import logging

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler to write the log messages to a file
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.DEBUG)

# Create a console handler to write the log messages to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter to format the log messages
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Add the formatter to the handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Test logging an error
try:
    x = 1 / 0
except Exception as e:
    logger.exception('An error occurred: %s', str(e))
