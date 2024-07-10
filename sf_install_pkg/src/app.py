import requests
import os
import json
import base64

import sys

from submodules.countriesIdentification import identify_locations
from submodules.datesIdentification import dates_binding
from submodules.magnitudeIdentification import magnitude_binding
from submodules.comparativesIdentification import comparatives_binding
from submodules.earthquaqeIdentification import identify_earthquake_event

from functools import wraps

from flask import Flask, request, jsonify, Response


app = Flask(__name__)

# Reading keycloak configuration
with open('/config/keycloak_configuration.json', 'r') as config_file:
    keycloak_config = json.load(config_file)

# Set up keycloak interface for the NL module part
kc_address = keycloak_config['URL']
realm = keycloak_config['realm']
client_name = keycloak_config['client_name']
admin_username = keycloak_config['adminUsername']
admin_password = keycloak_config['adminPassword']

def authenticate_user(username, password):
    # Request user token
    token_request_url = kc_address + f"realms/{realm}/protocol/openid-connect/token"
    token_request_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64.b64encode((client_name + ":" + keycloak_config['client_secret']).encode("utf-8")).decode("utf-8")
    }
    token_request_body = {
        "grant_type": "password",
        "client_id": client_name,
        "client_secret": keycloak_config['client_secret'],
        "password": password,
        "username": username
    }

    try:
        token_response = requests.post(token_request_url, headers=token_request_headers, data=token_request_body)
        token_data = token_response.json()
        if "error_description" in token_data:
            resp = token_data["error_description"]
            error = {"error": resp}
            return False

        token = token_data["access_token"]
        return True

    except requests.exceptions.RequestException as e:
        resp = "Error during token retrieval: " + str(e)
        error = {"error": resp}
        return False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not authenticate_user(auth.username, auth.password):
            return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated


# Define a custom function to replace the built-in print due to sychronazation issues
def custom_print(*args, **kwargs):
    # Print to stdout (console)
    print(*args, **kwargs)
    # Flush the stdout buffer to ensure immediate display
    sys.stdout.flush()


def process_final_dict(final_dictionary):
  """
  Function to convert each one of the error codes from each component into a relevant code number to be handled by the SF
  """
  # convert all tuple error messages into dictionary error messages
  for i, elem in enumerate(final_dictionary):
    if isinstance(elem, tuple):

      if elem == (0, "MAGNITUDE", "no_magnitude"):
        final_dictionary[i] = {"Number": 9999911}

      elif elem == (0, "MAGNITUDE", "more_magnitude"):
        final_dictionary[i] = {"Number": 9999912}

      elif elem == (0, "MAGNITUDE", "format_error"):
        final_dictionary[i] = {"Number": 9999914}

      elif elem == (0, "MAGNITUDE", "unknown_error"):
        final_dictionary[i] = {"Number": 9999913}

      elif elem == (0, "EARTHQUAKE_EVENT", "no_earthquake_reference"):
        final_dictionary[i] = {"event":9999921}

      elif elem == (0, "EARTHQUAKE_EVENT", "unknown_error"):
        final_dictionary[i] = {"event": 9999922}

      elif elem == (0,'DATES', 'wrong_date_format'):
        final_dictionary[i] = {"date": {"day": 9999931, "month": 9999931, "year": 9999931}}

      elif elem == (0,'DATES', 'no_date'):
        final_dictionary[i] = {"date": {"day": 9999932, "month": 9999932, "year": 9999932}}

      elif elem == (0,'DATES', 'more_dates'):
        final_dictionary[i] = {"date": {"day": 9999933, "month": 9999933, "year": 9999933}}

      elif elem == (0,'DATES', 'unknown_error'):
        final_dictionary[i] = {"date": {"day": 9999934, "month": 9999934, "year": 9999934}}

      elif elem == (0, "LOCATION", "no_country"):
        final_dictionary[i] = {"city":[9999941], "country":[9999941]}

      elif elem == (0, "LOCATION", "more_city_or_country"):
        final_dictionary[i] = {"city": [9999942], "country": [9999942]}

      elif elem == (0, "LOCATION", "more_country"):
        final_dictionary[i] = {"city": [9999943], "country": [9999943]}

      elif elem == (0, "LOCATION", "unknown_error"):
        final_dictionary[i] = {"city": [9999944], "country": [9999944]}

      elif elem == (0, "COMPARATIVES", "more_comparatives_mentions"):
        final_dictionary[i] = {"comparative": 9999951}

      elif elem == (0, "COMPARATIVES", "no_comparatives"):
        final_dictionary[i] = {"comparative": 9999952}

      elif elem == (0, "COMPARATIVES", "more_symbol_comparatives"):
        final_dictionary[i] = {"comparative": 9999953}

      elif elem == (0, "COMPARATIVES", "unknown_error"):
        final_dictionary[i] = {"comparative": 9999954}

  return final_dictionary



def natural_language_module(sentence):
  """
  Function to execute the complete natural language module pipeline
  """
  try:
    final_dictionary = []

    # identify whether the sentence is referred on earthquake events
    earth_event = identify_earthquake_event(sentence)

    if earth_event:
      final_dictionary.append(earth_event)

    # identify the target country and city in the sentence
    location = identify_locations(sentence)

    if location:
      final_dictionary.append(location)

    # identify the target comparative in the sentence
    comparative = comparatives_binding(sentence)

    if comparative:
      final_dictionary.append(comparative)

    # identify the target date in the sentence
    date = dates_binding(sentence)

    if isinstance(date, list):

        date_dict = date[0]
        date_replc = date[1]

        if date_dict:
          final_dictionary.append(date_dict[0])

          # we also delete the date reference from the sentence so that there will
          # not be any confusion with it for the magnitude identification module
          if len(date_replc) == 1:
            sentence = sentence.replace(date_replc[0], " ")

    # in case it is a tuple we add it as it is and we do not substitute something in the sentence
    elif isinstance(date, tuple):
      final_dictionary.append(date)

    # identify the target magnitude number in the sentence
    magnitude = magnitude_binding(sentence)

    if magnitude:
      final_dictionary.append(magnitude)

    clean_final_dictionary = process_final_dict(final_dictionary)

    result = {}
    for d in clean_final_dictionary:
      result.update(d)

    return result

  except:
    return "\n\n=== AN UNEXPECTED ERROR HAS OCCURED. PLEASE EXECUTE AGAIN THE SCRIPT OR COMMUNICATE WITH THE DEVELOPER TEAM === \n\n"


def replace_zero_with_null(d):
  """
  This is a small helper function to convert the 0 references on the final json to be sent, into None, as needed by the SF
  """
  for k, v in d.items():
    if isinstance(v, dict):
      replace_zero_with_null(v)
    elif (v == 0 or v == '0') and k != "point":
      d[k] = "null"
  return d


def process_json_sf(nl_json, sentence):
  """
  Function to convert the captured information an a relevant json format
  """
  try:

    # Format country and city in a proper way for the JSON file
    if isinstance(nl_json['country'][0], str) and not (nl_json['country'][0] == "null" or nl_json['country'][0] == "Null"):
        target_country = nl_json['country'][0].title()
    else:
        target_country = nl_json['country'][0]


    if isinstance(nl_json['city'][0], str) and not (nl_json['city'][0] == "null" or nl_json['city'][0] == "Null"):
        target_city = nl_json['city'][0].title()
    else:
        target_city = nl_json['city'][0]

    if nl_json['country'][0] == "Uk":
        target_country = "United Kingdom"

    if nl_json['country'][0] == "Usa":
        target_country = "United States"

    if nl_json['country'][0] == "Uae":
        target_country = "United Arab Emirates"

    sf_json_format = {
      "text": sentence,
      "page": "1",
      "nlp": {"event": nl_json['event'], "city": target_city, "country": target_country, "year": int(nl_json['date']['year']), "month": int(nl_json['date']['month']),
              "day": int(nl_json['date']['day']), "magnitude": nl_json['Number'], "comparative": nl_json['comparative'], "point": False, "latitude": "null", "lognitude": "null"}
    }

    return sf_json_format

  except:
    return "\n\n=== AN UNEXPECTED ERROR HAS OCCURED. PLEASE EXECUTE AGAIN THE SCRIPT OR COMMUNICATE WITH THE DEVELOPER TEAM === \n\n"



def send_json_to_endpoint(json_output, username, password):
  """
  Function to send the produced json to a target endpoint
  """
  headers = {'Content-type': 'application/json'}
  auth = (username, password)

  response = requests.post(os.environ.get('SF_ENDPOINT', 'http://sf-api2:8080/SemanticFramework/api/retrieve'), json=json_output, headers=headers, auth=auth)

  if response.status_code == 200:
    return response
  else:
    print("\n\nERROR SENDING JSON TO ENDPOINT. PLEASE TRY AGAIN OR CONTACT THE DEVELOPER TEAM.\n\n")



@app.route(os.environ.get('NL_ENDPOINT', '/NaturalLanguage'), methods=['POST'])
@requires_auth
def process_natural_language():
  """
  Function to process a sentence and return a JSON response
  """
  try:
      sentence = request.json['text']

      username = request.authorization.username
      password = request.authorization.password

      nl_data = natural_language_module(sentence)
      nl_json = process_json_sf(nl_data, sentence)
      nl_json_with_null = replace_zero_with_null(nl_json)

      # Modify the "city" value in nl_json_with_null
      if nl_json_with_null['nlp']['city'] == "null":
          nl_json_with_null['nlp']['city'] = 9999945

      sf_data = send_json_to_endpoint(nl_json_with_null, username, password)

      with open('/config/nl_logger_config.json', 'r') as file:
        config_data = json.load(file)

      # Get the value of the nl_logger field
      nl_logger = config_data['nl_logger']

      if nl_logger:
        custom_print("\n\nThis is the output of the NL module:")
        custom_print(nl_json_with_null)
        custom_print("\n\n")

      try:
          response = json.loads(sf_data.content.decode('utf-8'))
          return jsonify(response)

      except AttributeError:
          response = {
              'SF_response': []
          }

          return jsonify(response)

  except:

      response = {
          'SF_response': "error: Something unexpected happened. Please contact with the developer team."
      }

      return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)