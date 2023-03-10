import json
import logging
import os
import requests
import time

from json.decoder import JSONDecodeError

# Import the handle_message function from your main code file
from main import handle_message


# Set up logging
logging.basicConfig(level=logging.DEBUG)

def application(environ, start_response):
    # Set the response content type
    headers = [("Content-type", "application/json")]

    # Get the request method and path from the environment
    method = environ.get("REQUEST_METHOD")
    path = environ.get("PATH_INFO")

    if method == "POST" and path == "/":
        try:
            # Get the request body
            length = int(environ.get("CONTENT_LENGTH", "0"))
            body = environ["wsgi.input"].read(length).decode()

            # Parse the request body as JSON
            request = json.loads(body)

            # Call the handle_message function with the request and an empty conversation history
            response = handle_message(request, "")

            # Construct the response data as a JSON string
            data = json.dumps({"response": response})

            # Set the response status code and send the response data
            status = "200 OK"
            start_response(status, headers)
            return [data.encode()]

        except JSONDecodeError:
            # If the request body cannot be parsed as JSON, return a 400 Bad Request response
            status = "400 Bad Request"
            start_response(status, headers)
            return [json.dumps({"error": "Invalid request body"}).encode()]

    else:
        # If the request method or path is not supported, return a 404 Not Found response
        status = "404 Not Found"
        start_response(status, headers)
        return [json.dumps({"error": "Resource not found"}).encode()]
