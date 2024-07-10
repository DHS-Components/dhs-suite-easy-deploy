import spacy
import re

from datetime import datetime

# Load the spacy model with GloVe embeddings
nlp = spacy.load("en_core_web_lg")


# Define a function to extract dates from text
def extract_dates(text):
    """
    Identify dates both in numeric and free-text from text, using date regex patterns and NER tag
    """

    # Define regex patterns for common date formats
    # Regular expressions that include the \b word boundary character to ensure that the date pattern only matches if it is not part of a longer pattern that has already been matched
    date_patterns = [
        r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',  # Matches dates like "01/01/22" or "1-1-2022"
        r'\b\d{1,2}[-/]\d{1,2}\b(?!\d)',  # Matches dates like "01/01" or "1-1"
        r'\b[A-Z][a-z]{2,8} \d{1,2},? \d{2,4}\b',  # Matches dates like "January 1, 2022" or "Feb 28, 22"
        r'\b\d{1,2} [A-Z][a-z]{2,8} \d{2,4}\b',  # Matches dates like "1 January 2022" or "28 Feb 22"
        r'\b[A-Z][a-z]{2,8} \d{2,4}\b',  # Matches dates like "January 2022" or "Feb 22"
        r'\d{1,2}[/-]\d{4}|\d{2}\s\d{4}'
        # Matches dates like (05/2018, 05-2018, 05 2018, 5/2018, 5-2018, 5 2018, 05/18, 05-18, 05 18, 5/18, 5-18, 5 18) etc.

    ]

    # Find all matches for date patterns in the text
    matches = []
    for pattern in date_patterns:
        for match in re.findall(pattern, text):

            # Check if the match is part of a longer date pattern that has already been matched
            if all(match not in m for m in matches):
                matches.append(match)

    # Use SpaCy to extract additional dates
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == 'DATE':
            date_str = ent.text

            # Checks each SpaCy date reference against the matches list to ensure that it is not already included
            if all(date_str not in m for m in matches):
                matches.append(date_str)

    # Remove duplicates and return the matches
    return list(set(matches))

def helper_fix_format_date_sf(input_list):

    input_str = input_list[0]

    # Split the string into separate key-value pairs
    pairs = input_str.split(", ")
    pairs_dict = {}

    # Convert the key-value pairs into a dictionary
    for pair in pairs:
        key, value = pair.split(":")
        pairs_dict[key] = value

    # Create a list of dictionaries, ensuring all keys are present
    output_list = {"day": pairs_dict.get("day", 0),
                   "month": pairs_dict.get("month", 0),
                   "year": pairs_dict.get("year", 0)}

    return [{"date":output_list}]


def convert_dates(date_list):
    """
    Assign to the identified formatted dates the proper date format and then, on the formatted dates, assign the relevant date tags (e.g. specify which is the day, the month, etc)
    """

    DATE_FORMATS = {
        '%B %d, %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%-m-%d-%Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%m-%d-%y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%d/%m': 'day:{dt.day}, month:{dt.month}',
        '%B %d': 'day:{dt.day}, month:{dt.month}',
        '%b %d': 'day:{dt.day}, month:{dt.month}',
        '%B %Y': 'month:{dt.month}, year:{dt.year}',
        '%Y': 'year:{dt.year}',
        '%d/%m/%y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%B %d, %y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%b %d, %y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%d-%m-%Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%d/%m/%Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%d-%m-%y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%m/%d/%y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%m/%d/%Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%m-%d-%Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%m-%d-%y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%d/%m/%Y %H:%M:%S': 'day:{dt.day}, month:{dt.month}, year:{dt.year}, time:{dt.strftime("%H:%M:%S")}',
        '%d/%m/%y %H:%M:%S': 'day:{dt.day}, month:{dt.month}, year:{dt.year}, time:{dt.strftime("%H:%M:%S")}',
        '%m/%d/%Y %H:%M:%S': 'day:{dt.day}, month:{dt.month}, year:{dt.year}, time:{dt.strftime("%H:%M:%S")}',
        '%m/%d/%y %H:%M:%S': 'day:{dt.day}, month:{dt.month}, year:{dt.year}, time:{dt.strftime("%H:%M:%S")}',
        '%Y-%m-%d': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%y-%m-%d': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%m-%d-%Y %H:%M:%S': 'day:{dt.day}, month:{dt.month}, year:{dt.year}, time:{dt.strftime("%H:%M:%S")}',
        '%m-%d-%y %H:%M:%S': 'day:{dt.day}, month:{dt.month}, year:{dt.year}, time:{dt.strftime("%H:%M:%S")}',
        '%m-%d': 'month:{dt.month}, day:{dt.day}',
        '%-m-%-d': 'month:{dt.month}, day:{dt.day}',
        '%d %b %y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%d %B %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%b %Y': 'month:{dt.month}, year:{dt.year}',
        '%b %d, %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%d %B %y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',

        # 09 05 2018
        '%d %m %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',

        # 05/2018, 05-2018, 05 2018, 5/2018, 5-2018, 5 2018
        '%m %Y': 'month:{dt.month}, year:{dt.year}',
        '%m/%Y': 'month:{dt.month}, year:{dt.year}',
        '%m-%Y': 'month:{dt.month}, year:{dt.year}',

        # 05/18, 05-18, 05 18, 5/18, 5-18, 5 18
        '%m/%y': 'month:{dt.month}, year:{dt.year}',
        '%m-%y': 'month:{dt.month}, year:{dt.year}',
        '%m %y': 'month:{dt.month}, year:{dt.year}',
        '%-m/%y': 'month:{dt.month}, year:{dt.year}',
        '%-m-%y': 'month:{dt.month}, year:{dt.year}',
        '%-m %y': 'month:{dt.month}, year:{dt.year}',

        # 9th May 2018 etc
        '%dth %B %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%dth %b %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%dst %B %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%dst %b %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%dnd %B %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%dnd %b %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%drd %B %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%drd %b %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',

        # August 9 2018, August 9 18, Jan 1 23, etc.
        '%B %d %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%B %d %y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%b %d %y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}',
        '%b %d %Y': 'day:{dt.day}, month:{dt.month}, year:{dt.year}'
    }

    output_list = []
    for date_str in date_list:
        valid_format = False
        for fmt, out_fmt in DATE_FORMATS.items():
            try:
                dt = datetime.strptime(date_str, fmt)
                output_list.append(out_fmt.format(dt=dt))
                valid_format = True
                break
            except ValueError:
                pass
        if not valid_format:
            # Attempt to parse using a custom format
            try:
                if '-' in date_str:
                    dt = datetime.strptime(date_str, '%m-%d-%y')
                else:
                    dt = datetime.strptime(date_str, '%d/%m/%y')
                output_list.append(f'day:{dt.day}, month:{dt.month}, year:{dt.year}')
            except ValueError:
                output_list.append(f'INVALID FORMAT: {date_str}')

    # return output_list
    return helper_fix_format_date_sf(output_list)


def dates_binding(text):
  '''
  This is a function that binds together all the subcomponents of the dates identification, while also controlling for multiple, or zero date references
  '''

  try:

      # capture the referred dates
      ident_dates = extract_dates(text)

      # since we now cope for formats like '05 2018' and '09 05 2018', our module would capture them as two seperate cases.
      # with this line we check if '05 2018' is contained on '09 05 2018', in which case we delete it
      identified_dates = [elem for elem in ident_dates if not any(elem in other_elem for other_elem in ident_dates if elem != other_elem)]

      # we only accept for one date reference
      if len(identified_dates) == 1:

        formatted_dates = convert_dates(identified_dates)

        # in case there is a wrong date format then return the appropriate code to prompt back the proper message
        if 'INVALID FORMAT' in formatted_dates[0]:
          return (0,'DATES','wrong_date_format')

        else:
          return [formatted_dates, identified_dates]

      # in case of zero references return the appropriate code (to aid returning the correct prompt)
      elif len(identified_dates) == 0:
        return (0,'DATES','no_date')

      # in case of more than one references return the appropriate code (to aid returning the correct prompt)
      elif len(identified_dates) > 1:
        return (0,'DATES','more_dates')

      # in case of unexpected error return the appropriate code (to aid returning the correct prompt)
      else:
        return (0,'DATES','unknown_error')

  except:
      return (0,'DATES','unknown_error')


