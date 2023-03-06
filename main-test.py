# "MYSHLENEK",
# writen by Sergei Sychev in cooperation with ChatGPT
# Beta, 0062.02.2023 (this version without the 'settings.py' file)

####################################

# THE PURPOSE OF THE SCRIPT "MYSHLENEK"

# This script is a bot designed to generate responses to User input based on the conversation history
# using OpenAI's text-generation API.

# It interfaces with the Telegram API to receive and send messages to Users,
# while logging events and errors to a file and the console.

####################################

# ALL THE PARTS OF THE SCRIPT

# The script consists of the 4 functions: 'SEND_MESSAGE', 'GENERATE_RESPONSE', 'HANDLE_MESSAGE' and 'GET_UPDATES',
# which are described in details below.

# The script also has the 'POLL_INTERVAL' constant and the 'MAIN LOOP'. Both are described in details below.

# It also has the logging system, described in details below as well.

####################################

# THE DATA FLOW

# 1. The Telegram API sends messages to the bot as updates.

# This means that when a User sends a message to the bot on Telegram,
# the Telegram API sends the message as an update to the bot,
# which is then retrieved and processed by the script.

# 2. The 'GET_UPDATES' function retrieves the updates from the Telegram API
# using the 'requests' library and returns them as a list of update dictionaries.

# 3. The 'MAIN LOOP' retrieves the updates returned by 'GET_UPDATES' function
# and passes them to the 'HANDLE_MESSAGE' function one by one.

# 4. The 'HANDLE_MESSAGE' function extracts the text of the message from the update dictionary
# and passes it to the 'GENERATE_RESPONSE' function along with the conversation history.

# 5. The 'GENERATE_RESPONSE' function sends a request to the OpenAI API
# to generate a response using the provided prompt and returns the generated text.

# 6. The generated text is added to the conversation history and sent back to the user as a response
# using the 'SEND_MESSAGE' function.

# 7. If an error occurs at any point during the process,
# the error message and traceback are logged using the 'logger.exception()' method, described below.

# 8. The 'GET_UPDATES' function, the 'HANDLE_MESSAGE' function, and the 'GENERATE_RESPONSE' function
# all use the logger object to log messages and errors to the console and a log file.

# 9. The 'POLL_INTERVAL' constant is used for the 'MAIN LOOP'
# to control the frequency of polling for updates from the Telegram API.

# Overall, the data flow in the script involves retrieving updates from the Telegram API,
# generating a response using the OpenAI API, and sending the response back to the user.

# The flow is controlled by the 'MAIN LOOP' that polls the Telegram API for updates at a specified interval
# and passes them to the appropriate functions for processing.

# Error handling and logging are used throughout the process to help diagnose any issues that arise.

####################################

# THE EXTERNAL LIBRARIES AND FILES in use:

import os
import logging
import json
import requests
import time
from json.decoder import JSONDecodeError

####################################

# THE VARIABLE ENVIRONMENT

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')
API_HASH = os.getenv('API_HASH')
API_ID = os.getenv('API_ID')

####################################

# THE LOGGING CONFIGURATION SECTION

# The logging module is used to log debug and error messages to the console and a file named "error.log".
# The logger is set to the debug level,
# and both a console and file handler are added to the logger to handle the logging.
# The file handler is set to log at the debug level and is used to write messages to the "error.log" file.
# The console handler is also set to log at the debug level and writes messages to the console.
# The format of the log message is set using a formatter that includes the timestamp, log level, and message.

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter to format the log messages
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Create a file handler to write the log messages to a file
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Create a console handler to write the log messages to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# As you can see below, the script uses the 'logger.exception' method.
# This method of the logging module in Python is used
# to log an error message along with the stack trace of the exception that caused the error.

# It is a convenience method that allows developers to log both the error message
# and the traceback in a single line of code.

# The logger.exception() method works by first logging the error message as it would with the logger.error() method.
# It then adds the traceback information for the exception that caused the error to the log message.
# This is useful for debugging, as it provides a full picture of what went wrong in the code.

# The main difference between the logger.exception() method and other logging methods,
# like logger.error() or logger.debug() is that
# the former automatically includes the traceback information for any exceptions that occurred.
# This makes it very useful for debugging purposes,
# as it allows developers to quickly see where an error occurred and how it was triggered.

# In the script, the logger.exception() method is used extensively
# to log errors and exceptions that occur during the execution of the code.
# For example, it is used to log errors related to missing fields in update dictionaries, failed API requests,
# and invalid input data.

# By logging these errors using the logger.exception() method,
# the script is able to provide a detailed error message along with the traceback information,
# which makes it easier to debug any issues that arise.

# One peculiarity of its application in this script is that it is used not only to log errors,
# but also to log various other messages related to the execution of the code.
# For example, it is used to log the received message, the conversation history, and the generated response.
# This use of logger.exception() may be somewhat unconventional, as it is typically used to log error messages.
# However, in this case, it provides a convenient way to log a message along with the traceback information,
# which can be useful for debugging purposes.

####################################

# THE "SEND_MESSAGE" FUNCTION

# This function sends a message to the User with the help of Telegram API.
# The function takes a string argument 'text', which represents the message to be sent.
# If the 'text' argument is empty, an error message is logged, and the function returns None.

# The Telegram API URL is constructed using the Telegram API key, chat ID, and the 'text' argument.

# A POST request is then sent to the Telegram API, and the response is checked for any HTTP errors.
# If there is an error, an error message is logged, and the function returns None.
# If the response is successful, the JSON data from the response is parsed,
# and if the 'ok' key in the JSON data is True, the response JSON is returned.
# Otherwise, an error message is logged, and the function returns None.


def send_message(text):
    # Check if the message text is empty
    if not text:
        # If the message text is empty, log an error message and return None
        error_msg = "Empty message text provided"
        logger.error(error_msg)
        return None

    # Construct the Telegram API URL using the Telegram API key and chat ID, and the message text
    url = 'https://api.telegram.org/bot' + TELEGRAM_API_KEY + '/sendMessage?chat_id=' + CHAT_ID + '&text=' + text

    # Send a POST request to the Telegram API with the constructed URL
    response = requests.post(url)

    # Check if the response has an HTTP error status code
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # If the response has an HTTP error status code,
        # log an error message with the status code and response text, and return None
        error_msg = "HTTP error occurred: {}".format(e)
        logger.exception(error_msg)
        logger.exception("Response text: {}".format(response.text))
        return None

    # Try to parse the response JSON data
    try:
        response_json = response.json()
    except json.JSONDecodeError as e:
        # If the response JSON data cannot be parsed,
        # log an error message with the decoding error and raw response text, and return None
        error_msg = "Error decoding response from Telegram: {}".format(e)
        logger.exception(error_msg)
        logger.exception("Raw response from Telegram: {}".format(response.text))
        return None

    # Check if the response JSON data has an 'ok' field with a value of True
    if not response_json.get('ok'):
        # If the response JSON data does not have an 'ok' field with a value of True,
        # log an error message with the response JSON data, and return None
        error_msg = "Telegram API returned an error: {}".format(response_json)
        logger.exception(error_msg)
        return None
    # If the function has not returned None by this point, the message has been successfully sent,
    # so return the response JSON data
    return response_json

####################################

# THE "GENERATE_RESPONDS" FUNCTION

# This function generates a response to a given prompt using OpenAI's text-generation API.
# The function takes in two arguments, 'prompt' and 'conversation_history'.
# The prompt argument is a string that represents the starting point of the conversation,
# while conversation_history is a list of strings that contains the previous conversation history.


def generate_response(prompt, conversation_history):
    # Checks if the conversation_history is a string, and if it is not, joins the list using a newline character
    # to create a string. Similarly, it converts the prompt variable to a string if it is not already a string.
    if not isinstance(conversation_history, str):
        conversation_history = '\n'.join(conversation_history)
    if not isinstance(prompt, str):
        prompt = str(prompt)
    # Log the prompt that is being sent to the OpenAI API
    logger.error("Prompt: %s", prompt)

    # Remove carriage return characters from conversation history and prompt
    conversation_history = conversation_history.replace('\r', '')
    prompt = prompt.replace('\r', '')

    # Remove any trailing white space from the conversation history
    conversation_history = conversation_history.rstrip()

    # Remove unnecessary instance of the prompt from the conversation history
    if prompt in conversation_history:
        conversation_history = conversation_history.replace(prompt, '', 1)

    # Concatenate the 'prompt' and 'conversation_history' variables.
    # If the conversation_history is not empty and the prompt does not start with the stripped conversation_history,
    # the function concatenates the two variables with a newline character.
    # If the conversation_history is not empty and the prompt does not start with the stripped conversation_history
    # followed by a newline character, the function concatenates the prompt variable with the conversation_history
    # variable using the length of the conversation_history variable to slice the prompt.
    logger.error("Before concatenation: prompt = %s conversation_history = %s", prompt, conversation_history)
    if conversation_history and not prompt.startswith(conversation_history.strip()):
        prompt = conversation_history.strip() + '\n' + prompt.lstrip()
        conversation_history += '\n' + prompt.lstrip()
    elif conversation_history:
        prompt = conversation_history.strip() + prompt[len(conversation_history):].lstrip()
    logger.error("After concatenation: prompt = %s conversation_history = %s", prompt, conversation_history)

    # Sends a request to the OpenAI API to generate a response using the provided prompt.
    # It creates a dictionary of parameters to be sent to the API.
    # It also sets the headers for the API request, including the content type and authorization key.
    data = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "temperature": 0.9,
        "max_tokens": 3900,
        "top_p": 1,
        "n": 1
    }

    # Convert the data to a JSON string
    json_data = json.dumps(data)

    # Validate the query before sending it
    try:
        json.loads(json_data)
        logger.error("Data sent to OpenAI API: %s", data)
    except ValueError:
        error_msg = "Invalid request data:{}".format(json_data)
        logger.exception(error_msg)
        return "Seems, something happened, sorry."

    # Set the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(OPENAI_API_KEY)
    }

    # Log the request data before sending it
    logger.error("Sending request to OpenAI with data: %s", data)

    # Sends the API request using the requests library and checks the status code of the response.
    # If the status code is 200, it parses the response JSON and returns the generated text from the API.
    # If the status code is not 200, the function returns "Seems, something happened, sorry".
    response = requests.post('https://api.openai.com/v1/completions', json=data, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if len(response_data['choices']) > 0:
            return response_data['choices'][0]['text']
    else:
        error_msg = "OpenAI API request failed with status code {}".format(response.status_code)
        logger.exception(error_msg)
        return "Seems, something happened, sorry."

    # Add logging for successful response
    generated_response = response_data['choices'][0]['text']
    logger.error("Generated response: %s", generated_response)

    # If the function has not returned by this point, an error occurred
    # and it returns "Seems, something happened, sorry"
    error_msg = "OpenAI API request failed with status code {}".format(response.status_code)
    print("Error message:", error_msg)
    logging.error("Error message: %s", error_msg)
    logger.exception("Something went wrong while generating a response")
    return "Seems, something happened, sorry"

####################################

# THE "HANDLE_MESSAGE" FUNCTION

# This function handles incoming messages from the Telegram API.
# It handles a message received from the User and generates a response using the OpenAI API.

# The function takes two arguments, 'update' and 'conversation_history',
# with 'conversation_history' being an optional argument that is initialized as an empty string.
# The 'update' argument contains the data from the User's message,
# and the 'conversation_history' argument is a string containing the previous conversation history.


def handle_message(update, conversation_history=""):
    try:
        # Check if the update has a 'message' field and a 'text' field
        if 'message' not in update or 'text' not in update['message']:
            # If the update is missing the required fields, raise a ValueError with an error message
            raise ValueError("Error: The 'message' key or its 'text' subkey is missing from the update dictionary.")

        # Extract the text of the incoming message from the update dictionary
        text = update['message']['text']

        # Log the received message and conversation history
        received_message_msg = "Received message: {}".format(text)
        logger.exception(received_message_msg)
        conversation_history_msg = "Conversation history: {}".format(conversation_history)
        logger.exception(conversation_history_msg)

        # Add the received message to the conversation history if it is not empty
        if text.strip():
            conversation_history += '\n' + text

        # Log the prompt and conversation history before generating a response
        before_generate_response_msg = "Before generate_response(): prompt = {}, conversation_history = {}".format(text, conversation_history)
        logger.exception(before_generate_response_msg)

        # Generate a response using the incoming message as the prompt and the conversation history as context
        response = generate_response(text, conversation_history)

        # Log the generated response
        after_generate_response_msg = "After generate_response(): response = {}".format(response)
        logger.exception(after_generate_response_msg)

        # If a response was generated, add it to the conversation history
        if response is not None:
            conversation_history += '\n' + response  # add the response to the conversation history

        # Log the conversation history after adding the generated response
        after_concatenation_msg = "After concatenation: conversation_history = {}".format(conversation_history)
        logger.exception(after_concatenation_msg)

        # Send the generated response as a message to the Telegram API
        send_message(response)

    except (KeyError, ValueError) as e:
        # If an error occurs while handling the update,
        # log an error message with the error and return the current conversation history
        error_handling_update_msg = "Error handling update: {}".format(e)
        logger.exception(error_handling_update_msg)

    # Return the updated conversation history
    return conversation_history

####################################

# THE "GET_UPDATES" FUNCTION

# This function retrieves updates from the Telegram API using a GET request.
# The function takes an optional argument 'offset'
# which is used to specify the message offset to start retrieving updates from.
# If no offset is provided, the function retrieves all available updates.
# The function constructs the Telegram API URL using the Telegram API key and the 'getUpdates' method.
# The 'offset' parameter is added to the request parameters if it is provided,
# and a GET request is sent to the Telegram API.
# If the response status code is 200, the JSON data from the response is parsed,
# and the 'result' key is checked for any updates.
# If there are updates, they are returned as a list.
# Otherwise, an error message is logged, and an empty list is returned.


def get_updates(offset=None):
    # Construct the URL to retrieve updates from the Telegram API using the Telegram API key and offset
    url = "https://api.telegram.org/bot" + TELEGRAM_API_KEY + "/getUpdates"
    params = {}
    if offset:
        params['offset'] = offset

    # Send a GET request to the Telegram API with the constructed URL and optional offset parameter
    response = requests.get(url, params=params)
    renews = []

    # Check if the response has an HTTP status code of 200 (OK)
    if response.status_code == 200:
        try:
            # Try to parse the response JSON data and extract the 'result' field
            result = response.json()["result"]
        except JSONDecodeError as e:
            # If the response JSON data cannot be parsed,
            # log an error message with the decoding error and return an empty list
            error_msg = "Failed to decode JSON from Telegram API: {}".format(e)
            print("Error:", error_msg)
            logging.exception(error_msg)
            return renews

        # If the 'result' field is not empty, set the 'renews' list to the 'result' field
        if len(result) > 0:
            renews = result

        # Log a message with the 'result' field
        error_msg = "Result from Telegram API: {}".format(result)
        print(error_msg)
        logging.error(error_msg)
    else:
        # If the response has an HTTP status code other than 200,
        # log an error message with the status code and return an empty list
        error_msg = "Failed to get updates from Telegram API, status code: {}".format(response.status_code)
        print("Error:", error_msg)
        logging.exception(error_msg)

    # Return the 'renews' list of updates
    return renews

####################################

# THE "POLL_INTERVAL" LINE

# This independence line of the script defines a constant variable 'POLL_INTERVAL',
# which is used to specify the time interval (in seconds) between each poll for updates from the Telegram API.
# The comment in the code suggests that the value of this constant can be changed as desired
# to adjust the frequency of polling.

# Since this line is not part of either the main loop or the get_updates() function,
# it is executed when the script is loaded and before any of the other functions are called.
# Once the constant is defined, its value is used in the main loop to control the frequency of polling.


POLL_INTERVAL = 12  # Change the value as desired

####################################

# THE MAIN LOOP

# This main loop of the script continuously polls the Telegram API
# for updates every N seconds using the 'get_updates' function.

# If there are updates, the loop iterates over each update and calls the 'handle_message' function
# with the update and the conversation history.

# The conversation history is updated with the response generated by the 'handle_message' function.
# If there is an exception raised while handling the update, an error message is logged.

# The loop then sleeps for N seconds before polling the Telegram API again.

conversation_history = ""  # Initialize the conversation history as an empty string
last_update_id = 0 # Initialize the last update ID as 0
while True:
    # Poll the Telegram API for updates using the 'get_updates' function
    updates = get_updates(last_update_id)

    # If there are updates, iterate over each update and handle it using the 'handle_message' function
    if updates:
        for update in updates:
            update_id = update["update_id"]
            if update_id > last_update_id:
                last_update_id = update_id
                try:
                    conversation_history = handle_message(update, conversation_history)
                except Exception as e:
                    error_msg = "Error handling update: {}".format(e)
                    print("Error:", error_msg)
                    logging.exception(error_msg)

    # Sleep for N seconds before polling the Telegram API again
    time.sleep(POLL_INTERVAL)