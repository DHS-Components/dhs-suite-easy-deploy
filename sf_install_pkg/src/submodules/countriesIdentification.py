import spacy

from geopy.geocoders import Nominatim
import geonamescache
import pycountry

from geotext import GeoText

import re

from joblib import load
import os

# Load the spacy model with GloVe embeddings
nlp = spacy.load("en_core_web_lg")

# Load valid city names from geonamescache
gc = geonamescache.GeonamesCache()

# There is a bug with geonamescache where some countries exist as cities (e.g. albania)
# So initially we delete any country reference from the cities

# Get a list of all country names
original_countries = set(country['name'] for country in gc.get_countries().values())

# Get a list of all the original city names
original_cities = set(city['name'] for city in gc.get_cities().values())

# Get a list of all country names that appear as city names
country_names = set(
    country['name'] for country in gc.get_countries().values() if country['name'] not in original_cities)

# We also add these two cases because they have been asked by SERCO
country_names.add("Guinea Bissau")
country_names.add("Guinea bissau")
country_names.add("guinea Bissau")
country_names.add("guinea bissau")
country_names.add("Timor Leste")
country_names.add("Timor leste")
country_names.add("timor Leste")
country_names.add("timor leste")
country_names.add("UAE")
country_names.add("uae")
country_names.add("Uae")
country_names.add("Uk")
country_names.add("uK")
country_names.add("uk")
country_names.add("USa")
country_names.add("Usa")
country_names.add("usa")
country_names.add("uSa")
country_names.add("usA")
country_names.add("uSA")
country_names.add("Palestine")

# Get a list of all city names, excluding country names
city_names = set(city['name'] for city in gc.get_cities().values() if city['name'] not in original_countries)

city_names.add("Puebla de sanabria")


# === JSON cities parsing component === #

# Get a list of many countries/cities
cities_idf = gc.get_cities()
city_names_idf = [city['name'] for city in cities_idf.values()]

# Get the current directory of the file
current_directory = os.path.dirname(os.path.abspath(__file__))

# Create the path to the target folder
target_folder_path_locations = os.path.join(current_directory, "../json_data/location_list.joblib")

# Load city list from joblib file
loaded_location_list = load(target_folder_path_locations)

# keep countries and cities in seperate lists
countries_loc_json = []
cities_loc_json = []

for country, city in loaded_location_list:
    countries_loc_json.append(country)
    cities_loc_json.append(city)

# Remove leading and trailing whitespaces from city elements
stripped_cities_loc_json = [element.strip() for element in cities_loc_json]

cities_loc_set_json = []
for string in stripped_cities_loc_json:
    if string not in cities_loc_set_json:
        cities_loc_set_json.append(string)

# Remove leading and trailing whitespaces from country elements
stripped_countries_loc_json = [element.strip() for element in countries_loc_json]

countries_loc_set_json = []
for string in stripped_countries_loc_json:
    if string not in countries_loc_set_json:
        countries_loc_set_json.append(string)

# sort the final city list in descending order, based on the number of characters (in that way we avoid string matching of a subset of words etc)
cities_loc_set_sorted_json = sorted(cities_loc_set_json, key=lambda x: len(x), reverse=True)
countries_loc_set_sorted_json = sorted(countries_loc_set_json, key=lambda x: len(x), reverse=True)



def flatten(lst):
    """
    Define a helper function to flatten the list recursively
    """

    for item in lst:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def is_country(reference):
    """
    Check if a given reference is a valid country name
    """
    try:
        # Check if the reference is a valid city name from the first geoparse library
        if reference in country_names:
          return True

        else:
          # if not then use the pycountry library to verify if an input is a country
          country = pycountry.countries.search_fuzzy(reference)[0]

          temp_country_names = []

          if country:
            if hasattr(country, 'name') or hasattr(country, 'official_name') or hasattr(country, 'common_name'):

              if hasattr(country, 'official_name'):
                temp_country_names.append(country.official_name.lower())
              if hasattr(country, 'name'):
                temp_country_names.append(country.name.lower())
              if hasattr(country, 'common_name'):
                temp_country_names.append(country.common_name.lower())
              if any(reference.lower()==elem for elem in temp_country_names):
                return True

          return False

    except LookupError:
        return False


def is_city(reference):
    """
    Check if a given reference is a valid city name
    """

    reference = reference.replace("x$x", "").strip()

    # Check if the reference is a valid city name
    if reference in city_names:
        return True

    # Load the Nomatim (open street maps) api
    geolocator = Nominatim(user_agent="certh_serco_validate_city_app")
    location = geolocator.geocode(reference, language="en", timeout=10)


    # in case of None there was an error when trying location.raw
    if location == None:
        return False

    # If a reference is identified as a 'city', 'town', or 'village', then it is indeed a city
    if location.raw['type'] in ['city', 'town', 'village']:
        return True

    # If a reference is identified as 'administrative' (e.g. administrative area),
    # then we further examine if the retrieved info is a single token (meaning a country) or a series of tokens (meaning a city)
    # that condition takes place to separate some cases where small cities were identified as administrative areas
    elif location.raw['type'] == 'administrative':

        if len(location.raw['display_name'].split(",")) > 1:
            return True

    return False


def validate_locations(locations):
    """
    Validate that the identified references are indeed a Country and a City
    """

    validated_loc = []

    for location in locations:

        # validate whether it is a country
        if is_country(location):
            validated_loc.append((location, 'country'))

        # validate whether it is a city
        elif is_city(location):
            validated_loc.append((location, 'city'))

        else:
            # Check if the location is a multi-word name
            words = location.split()
            if len(words) > 1:

                # Try to find the country or city name among the words
                for i in range(len(words)):
                    name = ' '.join(words[i:])

                    if is_country(name):
                        validated_loc.append((name, 'country'))
                        break

                    elif is_city(name):
                        validated_loc.append((name, 'city'))
                        break

    return validated_loc


# JSON direct string matching

# helper function to know when to run the JSON string comparison for city
def check_city_reference(tuple_list):
    for item in tuple_list:
        if 'city' in item:
            return True
    return False

# helper function to know when to run the JSON string comparison for country
def check_country_reference(tuple_list):
    for item in tuple_list:
        if 'country' in item:
            return True
    return False


# Verify strict string comparison
def is_word_boundary(sentence, start_index, end_index):
    # Check if the start index is a word boundary
    if start_index > 0 and sentence[start_index - 1].isalpha():
        return False

    # Check if the end index is a word boundary
    if end_index < len(sentence) - 1 and sentence[end_index + 1].isalpha():
        return False

    return True


# function to identify city references based on string comparison and the entries of the JSON file
def identify_cities_with_json(city_list, sentence):

    # Initialize list to store matched city names
    matched_cities = []

    # for each city in my list, examine if it exists in the ordered city list (first it will examine the multi word entries, and then the single word ones)
    for city in city_list:
        pattern = r'\b' + re.escape(city.lower()) + r'\b'
        if re.search(pattern, sentence.lower()):
            matched_cities.append(city)

    # Return the matched countries if any, or None if none were found
    if matched_cities:
        return True, matched_cities
    else:
        return False, None


# function to identify countries references based on string comparison and the entries of the JSON file
def identify_countries_with_json(country_list, sentence):

    # Initialize list to store matched country names
    matched_countries = []

    # for each country in my list, examine if it exists in the ordered country list (first it will examine the multi word entries, and then the single word ones)
    for country in country_list:
        pattern = r'\b' + re.escape(country.lower()) + r'\b'
        if re.search(pattern, sentence.lower()):

            matched_countries.append(country)

    # Return the matched countries if any, or None if none were found
    if matched_countries:
        return True, matched_countries
    else:
        return False, None

# ##############################



def identify_loc_ner(sentence):
    """
    Identify all the geopolitical and location entities with the spacy tool
    """
    doc = nlp(sentence)

    ner_locations = []

    # GPE and LOC are the labels for location entities in spaCy
    for ent in doc.ents:
        if ent.label_ in ['GPE', 'LOC']:

            if len(ent.text.split()) > 1:
                ner_locations.append(ent.text)
            else:
                for token in ent:
                    if token.ent_type_ == 'GPE':
                        ner_locations.append(ent.text)
                        break

    return ner_locations


def identify_loc_geoparselibs(sentence):
    """
    Identify cities and countries with 3 different geoparsing libraries
    """

    geoparse_locations = []

    # Geoparsing library 1

    # Load geonames cache to check if a city name is valid
    gc = geonamescache.GeonamesCache()

    # Get a list of many countries/cities
    countries = gc.get_countries()
    cities = gc.get_cities()

    city_names = [city['name'] for city in cities.values()]
    country_names = [country['name'] for country in countries.values()]

    # if any word sequence in our sentence is one of those countries/cities identify it
    words = sentence.split()
    for i in range(len(words)):
        for j in range(i + 1, len(words) + 1):
            word_seq = ' '.join(words[i:j])
            if word_seq in city_names or word_seq in country_names:
                geoparse_locations.append(word_seq)

    # Geoparsing library 2

    # similarly with the pycountry library
    for country in pycountry.countries:
        if country.name in sentence:
            geoparse_locations.append(country.name)

    # Geoparsing library 3

    # similarly with the geotext library
    places = GeoText(sentence)
    cities = list(places.cities)
    countries = list(places.countries)

    if cities:
        geoparse_locations += cities
    if countries:
        geoparse_locations += countries

    return (geoparse_locations, countries, cities)


def identify_loc_regex(sentence):
    """
    Identify cities and countries with regular expression matching
    """

    regex_locations = []

    # Country and cities references can be preceded by 'in', 'from' or 'of'
    pattern = r"\b(in|from|of)\b\s([\w\s]+)"
    additional_refs = re.findall(pattern, sentence)

    for match in additional_refs:
        regex_locations.append(match[1])

    return regex_locations



def multiple_country_city_identifications_solve(country_city_dict):
    """
    This is a function to solve the appearance of multiple identification of countries and cities.
    It checks all the elements of the input dictionary and if any smaller length element exists as a substring inside
    a bigger length element of it, it deletes the smaller size one. In that sense, a dictionary of the sort
    {'city': ['Port moresby', 'Port'], 'country': ['Guinea', 'Papua new guinea']} will be converted into
    {'city': ['Port moresby'], 'country': ['Papua new guinea']}.

    The reason for that function, is because such type of incosistencies were identified during country/city identification,
    propably relevant to the geoparsing libraries in use
    """

    try:

        country_flag = False
        city_flag = False

        # to avoid examining any element in any case, we validate that both a country and a city exist
        # on the input dictionary and that they are of length more than one (which is the target case for us)
        if 'country' in country_city_dict:
            if len(country_city_dict['country']) > 1:
                country_flag = True

        if 'city' in country_city_dict:
            if len(country_city_dict['city']) > 1:
                city_flag = True

        # at first cope with country multiple iterative references
        if country_flag:

            # Sort the countries by length, longest first
            country_city_dict['country'].sort(key=lambda x: len(x), reverse=True)

            # Create a new list of countries that don't contain any substrings
            cleaned_countries = []
            for i in range(len(country_city_dict['country'])):
                is_substring = False
                for j in range(len(cleaned_countries)):
                    if country_city_dict['country'][i].lower().find(cleaned_countries[j].lower()) != -1:
                        # If the i-th country is a substring of an already-cleaned country, skip it
                        is_substring = True
                        break
                if not is_substring:
                    cleaned_countries.append(country_city_dict['country'][i])

            # Replace the original list of countries with the cleaned one
            country_city_dict['country'] = cleaned_countries

            # Create a new list of countries that are not substrings of other countries
            final_countries = []
            for i in range(len(country_city_dict['country'])):
                is_superstring = False
                for j in range(len(country_city_dict['country'])):
                    if i == j:
                        continue
                    if country_city_dict['country'][j].lower().find(country_city_dict['country'][i].lower()) != -1:
                        # If the i-th country is a substring of a different country, skip it
                        is_superstring = True
                        break
                if not is_superstring:
                    final_countries.append(country_city_dict['country'][i])

            # Replace the original list of countries with the final one
            country_city_dict['country'] = final_countries

        # then cope with city multiple iterative references
        if city_flag:

            # Sort the cities by length, longest first
            country_city_dict['city'].sort(key=lambda x: len(x), reverse=True)

            # Create a new list of cities that don't contain any substrings
            cleaned_cities = []
            for i in range(len(country_city_dict['city'])):
                is_substring = False
                for j in range(len(cleaned_cities)):
                    if country_city_dict['city'][i].lower().find(cleaned_cities[j].lower()) != -1:
                        # If the i-th city is a substring of an already-cleaned city, skip it
                        is_substring = True
                        break
                if not is_substring:
                    cleaned_cities.append(country_city_dict['city'][i])

            # Replace the original list of cities with the cleaned one
            country_city_dict['city'] = cleaned_cities

            # Create a new list of cities that are not substrings of other cities
            final_cities = []
            for i in range(len(country_city_dict['city'])):
                is_superstring = False
                for j in range(len(country_city_dict['city'])):
                    if i == j:
                        continue
                    if country_city_dict['city'][j].lower().find(country_city_dict['city'][i].lower()) != -1:
                        # If the i-th city is a substring of a different city, skip it
                        is_superstring = True
                        break
                if not is_superstring:
                    final_cities.append(country_city_dict['city'][i])

            # Replace the original list of cities with the final one
            country_city_dict['city'] = final_cities

        # return the final dictionary
        if country_city_dict:
            return country_city_dict

    except:
        return (0, "LOCATION", "unknown_error")


def helper_resolve_cities(sentence, locations):
    """
    Verify that the city captured does not belong to the capture country. If so delete it, unless there is also a second reference on the original sentence
    (which might be the case of a city with a similar name/substring of a country)
    """

    if 'country' in locations and 'city' in locations:

        # Check if any city names are also present in the corresponding country name
        for country in locations['country']:
            for city in locations['city']:

                if city.lower() in country.lower():
                    # If the city name is found in the country name, check how many times it appears in the sentence
                    city_count = len(re.findall(city, sentence, re.IGNORECASE))
                    if city_count == 1:
                        # If the city appears only once, remove it from the locations dictionary
                        locations['city'] = [c for c in locations['city'] if c != city]

    return locations


def helper_delete_city_reference(locations):
    """
    If the 'city' reference was captured by mistake by the system, delete it, unless it belongs to the cities that should contain it (e.g. Mexico city)
    """

    city_cities = ["Adamstown City", "Alexander City", "Angeles City", "Antipolo City", "Arizona City", "Arkansas City",
                   "Ashley City", "Atlantic City", "Bacolod City", "Bacoor City", "Bago City", "Baguio City",
                   "Baker City", "Baltimore City", "Batangas City", "Bay City", "Belgrade City", "Belize City",
                   "Benin City", "Big Bear City", "Bossier City", "Boulder City", "Brazil City", "Bridge City",
                   "Brigham City", "Brighton City", "Bristol City", "Buckeye City", "Bullhead City", "Butuan City",
                   "Cabanatuan City", "Calamba City", "Calbayog City", "California City", "Caloocan City",
                   "Calumet City", "Candon City", "Canon City", "Carcar City", "Carson City", "Castries City",
                   "Cathedral City", "Cavite City", "Cebu City", "Cedar City", "Central Falls City", "Century City",
                   "Cestos City", "City Bell", "City Terrace", "City of Balikpapan", "City of Calamba",
                   "City of Gold Coast", "City of Industry", "City of Isabela", "City of Orange", "City of Paranaque",
                   "City of Parramatta", "City of Shoalhaven", "Collier City", "Columbia City", "Commerce City",
                   "Cooper City", "Cotabato City", "Crescent City", "Crescent City North", "Culver City",
                   "Dagupan City", "Dale City", "Dali City", "Daly City", "Danao City", "Dasmariñas City", "Davao City",
                   "De Forest City", "Del City", "Dhaka City", "Dipolog City", "Dodge City", "Dumaguete City",
                   "El Centro City", "Elizabeth City", "Elk City", "Ellicott City", "Emeryville City", "Fernley City",
                   "Florida City", "Forest City", "Forrest City", "Foster City", "Freeport City", "Garden City",
                   "Gdynia City", "General Santos City", "General Trias City", "Gloucester City", "Granite City",
                   "Green City", "Grove City", "Guatemala City", "Haines City", "Haltom City", "Harbor City",
                   "Havre City", "Highland City", "Ho Chi Minh City", "Holiday City", "Horizon City", "Hyderabad City",
                   "Iligan City", "Iloilo City", "Imus City", "Iowa City", "Iriga City", "Isabela City", "Jacinto City",
                   "James City County", "Jefferson City", "Jersey City", "Jhang City", "Jincheng City", "Johnson City",
                   "Junction City", "Kaiyuan City", "Kansas City", "King City", "Kingman City", "Kingston City",
                   "Koror City", "Kowloon City", "Kuwait City", "Lake City", "Lake Havasu City", "Laoag City",
                   "Lapu-Lapu City", "Las Pinas City", "Las Piñas City", "League City", "Legazpi City", "Leisure City",
                   "Lenoir City", "Ligao City", "Lincoln City", "Linyi City", "Lipa City", "Loma Linda City",
                   "Lucena City", "Madrid City", "Makati City", "Malabon City", "Mandaluyong City", "Mandaue City",
                   "Manukau City", "Marawi City", "Marikina City", "Maryland City", "Mason City", "McKee City",
                   "Mexico City", "Mexico City Beach", "Michigan City", "Midwest City", "Mineral City", "Missouri City",
                   "Morehead City", "Morgan City", "Muntinlupa City", "Naga City", "Nagasaki City", "National City",
                   "Navotas City", "Nay Pyi Taw City", "Nevada City", "New City", "New York City", "Norwich City",
                   "Ocean City", "Oil City", "Oklahoma City", "Olongapo City", "Orange City", "Oregon City",
                   "Ozamiz City", "Pagadian City", "Palayan City", "Palm City", "Panabo City", "Panama City",
                   "Panama City", "Panama City Beach", "Parañaque City", "Park City", "Pasay City", "Peachtree City",
                   "Pearl City", "Pell City", "Phenix City", "Plant City", "Ponca City", "Port Augusta City",
                   "Port Pirie City", "Quad Cities", "Quartzsite City", "Quebec City", "Quezon City", "Quezon City",
                   "Rainbow City", "Rapid City", "Red City", "Redwood City", "Richmond City", "Rio Grande City",
                   "Roxas City", "Royse City", "Salt Lake City", "Salt Lake City", "Samal City", "San Carlos City",
                   "San Carlos City", "San Fernando City", "San Fernando City", "San Fernando City", "San Jose City",
                   "San Jose City", "San Juan City", "San Juan City", "San Pedro City", "Santa Rosa City",
                   "Science City of Munoz", "Shelby City", "Sialkot City", "Silver City", "Sioux City",
                   "South Lake Tahoe City", "South Sioux City", "Studio City", "Suisun City", "Summit Park City",
                   "Sun City", "Sun City Center", "Sun City West", "Sun City West", "Suva City", "Tabaco City",
                   "Tacloban City", "Tagbilaran City", "Taguig City", "Tagum City", "Talisay City", "Tanauan City",
                   "Tarlac City", "Tauranga City", "Tayabas City", "Temple City", "Texas City", "Thomas City",
                   "Tipp City", "Toledo City", "Traverse City", "Trece Martires City", "Tuba City", "Union City",
                   "Universal City", "University City", "Upper Hutt City", "Valencia City", "Valenzuela City",
                   "Vatican City", "Vatican City", "Ventnor City", "Webb City", "Wellington City", "Welwyn Garden City",
                   "West Valley City", "White City", "Yazoo City", "Yuba City", "Zamboanga City"]

    if 'city' in locations:
        for city in locations['city']:
            if 'city' in city:
                if not city in city_cities:
                    city = city.replace("city", "")

            elif 'City' in city:
                if not city in city_cities:
                    city = city.replace("City", "")

            locations['city'] = city

        # Convert city values to a list
        if isinstance(locations['city'], str):
            locations['city'] = [locations['city']]

    return locations


def helper_delete_country_reference(locations):
    """
    If the 'country' reference was captured by mistake by the system and exists in a city name, delete it
    """

    country_city_same = ["djibouti", "guatemala", "mexico", "panama", "san marino", "singapore", "vatican"]

    if 'country' in locations:
        for i, country in enumerate(locations['country']):

            if country.lower() not in country_city_same:
                split_country = country.lower().split()

                if 'city' in locations:
                    for j, city in enumerate(locations['city']):
                        split_city = city.lower().split()

                        for substring in split_country:
                            if substring in split_city:
                                split_city.remove(substring)
                                new_city = ' '.join(split_city)
                                locations['city'][j] = new_city.strip()

    return locations



def identify_locations(sentence):
    """
    Identify all the possible Country and City references in the given sentence, using different approaches in a hybrid manner
    """

    locations = []
    extra_serco_countries = False

    try:

        # this is because there were cases were a city followed by comma was not understood by the system
        sentence = sentence.replace(",", " x$x ")

        # Serco wanted to also handle these two cases without the symbol "-". The only way to do that is by hardcoding it
        if "Timor Leste" in sentence:
            extra_serco_countries = True
            locations.append("Timor Leste")

        if "Guinea Bissau" in sentence:
            extra_serco_countries = True
            locations.append("Guinea Bissau")

        # ner
        locations.append(identify_loc_ner(sentence))

        # geoparse libs
        geoparse_list, countries, cities = identify_loc_geoparselibs(sentence)
        locations.append(geoparse_list)

        # flatten the geoparse list
        locations_flat_1 = list(flatten(locations))

        # regex
        locations_flat_1.append(identify_loc_regex(sentence))

        # flatten the regex list
        locations_flat_2 = list(flatten(locations))

        # remove duplicates while also taking under consideration capitalization (e.g. a reference of italy should be valid, while also a reference of Italy and italy)
        # Lowercase the words and get their unique references using set()
        loc_unique = set([loc.lower() for loc in locations_flat_2])

        # Create a new list of locations with initial capitalization, removing duplicates
        loc_capitalization = list(
            set([loc.capitalize() if loc.lower() in loc_unique else loc.lower() for loc in locations_flat_2]))

        # That calculation checks whether there are substrings contained in another string. E.g. for the case of [timor leste, timor], it should remove "timor"
        if extra_serco_countries:
            loc_capitalization_cp = loc_capitalization.copy()
            for i, loc1 in enumerate(loc_capitalization):
                for j, loc2 in enumerate(loc_capitalization):
                    if i != j and loc1 in loc2:
                        loc_capitalization_cp.remove(loc1)
                        break

            loc_capitalization = loc_capitalization_cp

        # validate that indeed each one of the countries/cities are indeed countries/cities
        validated_locations = validate_locations(loc_capitalization)

        # ====== JSON PARSING =========

        json_city_flag, json_city = identify_cities_with_json(cities_loc_set_sorted_json, sentence)

        # if a city is found based on json parsing, perform an extra validation according to the target country
        if json_city_flag:

            # identify the country
            json_country_flag, json_country = identify_countries_with_json(countries_loc_set_sorted_json, sentence)

            # for each city we perform a valiation based on the coutnry (to avoid cases where Of is captured as a city since it is a substring,
            # while Turkey does not exist in the input query
            for city_elem in json_city:

                # if a country also exists, verify that the entry (city, country) is valid for the given json entries
                if json_country_flag:

                    for country_elem in json_country:

                        # check that the combination of country and city exists in the json, therefore is valid
                        if (country_elem, city_elem) in loaded_location_list:

                            validated_locations.append((city_elem, 'city'))

                # else if only city is found, just add it
                else:

                    validated_locations.append((city_elem, 'city'))

        # now also check seperately only for countries that were not recognized
        json_country_flag, json_country = identify_countries_with_json(countries_loc_set_sorted_json, sentence)

        if json_country_flag:

            for country_elem in json_country:
                validated_locations.append((country_elem, 'country'))

        # remove duplicates
        validated_locations_set = list(set((item[0].lower(), item[1].lower()) for item in validated_locations))

        # create a proper dictionary with country/city tags and the relevant entries as a result
        loc_dict = {}
        for location, loc_type in validated_locations_set:
            if loc_type not in loc_dict:
                loc_dict[loc_type] = []
            loc_dict[loc_type].append(location)

        # bring sentence on previous form
        sentence = sentence.replace(" x$x ", ",")

        # cope with cases of iterative country or city reference due to geoparse lib issues
        locations_dict = multiple_country_city_identifications_solve(loc_dict)

        if locations_dict == None:
            return (0, "LOCATION", "no_country")
            # return {'city':[], 'country':[]}

        else:
            # conditions for multiple references
            # it is mandatory that a country will exist
            if 'country' in locations_dict:

                # if a city exists
                if 'city' in locations_dict:

                    resolved_dict = helper_resolve_cities(sentence, locations_dict)

                    # we accept one country and one city
                    if len(resolved_dict['country']) == 1 and len(resolved_dict['city']) == 1:

                        # capitalize because there may be cases that it will return 'italy'
                        resolved_dict['country'][0] = resolved_dict['country'][0].capitalize()

                        # there were some cases that the 'x$x' was not removed
                        for key, values in resolved_dict.items():
                            for i, value in enumerate(values):
                                if 'x$x' in value:
                                    values[i] = value.replace('x$x', '')

                        delete_city = helper_delete_city_reference(resolved_dict)

                        return helper_delete_country_reference(delete_city)


                    # we can accept an absence of city but a country is always mandatory
                    elif len(resolved_dict['country']) == 1 and len(resolved_dict['city']) == 0:

                        resolved_dict['country'][0] = resolved_dict['country'][0].capitalize()
                        resolved_dict['city'] = ['0']

                        # there were some cases that the 'x$x' was not removed
                        for key, values in resolved_dict.items():
                            for i, value in enumerate(values):
                                if 'x$x' in value:
                                    values[i] = value.replace('x$x', '')

                        delete_city = helper_delete_city_reference(resolved_dict)

                        return helper_delete_country_reference(delete_city)

                    # error if more than one country or city
                    else:
                        return (0, "LOCATION", "more_city_or_country")


                # if a city does not exist
                else:
                    # we only accept for one country
                    if len(locations_dict['country']) == 1:

                        locations_dict['country'][0] = locations_dict['country'][0].capitalize()

                        # there were some cases that the 'x$x' was not removed
                        for key, values in locations_dict.items():
                            for i, value in enumerate(values):
                                if 'x$x' in value:
                                    values[i] = value.replace('x$x', '')

                        resolved_cities = helper_resolve_cities(sentence, locations_dict)
                        delete_city = helper_delete_city_reference(resolved_cities)

                        help_city = helper_delete_country_reference(delete_city)

                        if not 'city' in help_city:
                            help_city['city'] = [0]

                        return help_city

                    # error if more than one country
                    else:
                        return (0, "LOCATION", "more_country")

            # error if no country is referred
            else:
                return (0, "LOCATION", "no_country")

    except:
        # handle the exception if any errors occur while identifying a country/city
        return (0, "LOCATION", "unknown_error")