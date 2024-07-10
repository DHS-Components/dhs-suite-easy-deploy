import spacy
import re
from word2number import w2n

# Load the spacy model with GloVe embeddings
nlp = spacy.load("en_core_web_lg")


def capture_numbers(input_sentence):
    '''
      This is a function to capture cases of refered numbers either in numeric or free-text form
    '''

    try:
        # Define the regular expression patterns
        pattern1 = r"(\d+|\w+(?:\s+\w+)*)\s+(decimal|point|dot|comma)\s+(\d+|\w+(?:\s+\w+)*)"

        # Find all matches in the text
        matches = re.findall(pattern1, input_sentence)

        # This part is to capture cases like six point five, 5 point five, six point 5, 5 point 5
        pattern_numbers = []
        for match in matches:
            if len(match) == 3:
                # add the $pattern string to easily specify them in a subsequent step
                full_string = "{} {} {} {}".format(match[0], match[1], match[2], '$pattern')
                pattern_numbers.append(full_string)

        for elem in pattern_numbers:
            input_sentence = input_sentence.replace(elem, " ")

        if pattern_numbers:
            # Remove duplicates with set and convert back to list
            pattern_final_numbers = list(set(pattern_numbers))
        else:
            pattern_final_numbers = []

        # we delete the captured references from the sentence, because if we capture something like seven point five
        # then spacy will also identify seven and five, which we do not want it to
        for element in pattern_final_numbers:
            target_elem = element.replace("$pattern", "").strip()
            if target_elem in input_sentence:
                input_sentence = input_sentence.replace(target_elem, " ")

        # This is for cases of thirty eight or one million and two, etc.

        # Define a regular expression to match multiword free-text numbers
        pattern2 = r"(?<!\w)(?:(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|trillion)(?:\s(?:and\s)?(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|trillion))+\s?)+(?!\w*pennies)"

        # Find all multiword free-text number matches in the sentence
        multi_numbers = re.findall(pattern2, input_sentence)

        if multi_numbers:
            multinumber_final_numbers = list(set(multi_numbers))
        else:
            multinumber_final_numbers = []

        for elem in multinumber_final_numbers:
            if elem in input_sentence:
                input_sentence = input_sentence.replace(elem, " ")

        # we also delete the captured references from the sentence in this case
        for element in multinumber_final_numbers:
            target_elem = element.replace("$pattern", "").strip()
            if target_elem in input_sentence:
                input_sentence = input_sentence.replace(target_elem, " ")

        # Parse the input sentence with Spacy
        doc = nlp(input_sentence)

        # This is to capture all the numbers in int and float form, as well as numbers like eight, two, hundred
        s_numbers = [token.text for token in doc if token.like_num]

        if s_numbers:
            # Remove duplicates with set and convert back to list
            spacy_final_numbers = list(set(s_numbers))

        else:
            spacy_final_numbers = []

        # return the extracted numbers
        return pattern_final_numbers + multinumber_final_numbers + spacy_final_numbers

    except:
        return 0


def numeric_number_dot_freetext(text):
    '''
    This is a function to convert cases of '6 point five, six point 5 etc'
    '''

    try:
        # # Define a dictionary to map words to numbers
        num_dict = {
            'zero': 0,
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9,
            'ten': 10,
            'eleven': 11,
            'twelve': 12,
            'thirteen': 13,
            'fourteen': 14,
            'fifteen': 15,
            'sixteen': 16,
            'seventeen': 17,
            'eighteen': 18,
            'nineteen': 19,
            'twenty': 20,
            'thirty': 30,
            'forty': 40,
            'fifty': 50,
            'sixty': 60,
            'seventy': 70,
            'eighty': 80,
            'ninety': 90,
            'hundred': 100,
            'thousand': 1000,
            'million': 1000000,
            'billion': 1000000000,
            'trillion': 1000000000000
        }

        # # Define a regular expression pattern to extract the numeric form and free text form from input text
        pattern = r"(\d+|\w+(?:\s+\w+)*)\s+(?:decimal|point|dot|comma)\s+(\d+|\w+(?:\s+\w+)*)"

        # Use regular expression to extract the numeric form and free text form from input text
        match = re.search(pattern, text)

        if match:
            num1 = match.group(1)
            num2 = match.group(2)

            # If the numeric form is a word, map it to its numerical value
            if num1 in num_dict:
                num1 = num_dict[num1]

            # if not in the dictionary try also with the w2n library
            else:

                # try to convert to float. That means this is a number, otherwise it is a string so continue
                try:
                    num1 = float(num1)
                except:

                    # this will handle cases like "bla bla bla seven"
                    try:
                        num1 = w2n.word_to_num(num1)

                    # this is to handle cases like "bla bla bla 7"
                    except:

                        try:
                            # we identify all the numeric references
                            num_ref1 = [int(ref) for ref in re.findall(r'\d+', num1)]

                            # if there is exactly one number then we cope with that
                            if len(num_ref1) == 1:
                                num1 = num_ref1[0]

                            # in any other case throw an error
                            elif len(num_ref1) > 1:
                                return (0, 'MAGNITUDE', 'more_magnitude')

                            elif len(num_ref1) == 0:
                                return (0, 'MAGNITUDE', 'no_magnitude')

                        except:
                            return (0, 'MAGNITUDE', 'unknown_error')

            # If the free text form is a word, map it to its numerical value
            if num2 in num_dict:
                num2 = num_dict[num2]

            else:
                try:
                    num2 = int(num2)
                except:
                    try:
                        num2 = w2n.word_to_num(num2)
                    except:
                        try:
                            # we identify all the numeric references
                            num_ref2 = [int(ref) for ref in re.findall(r'\d+', num2)]

                            # if there is exactly one number then we cope with that
                            if len(num_ref2) == 1:
                                num2 = num_ref2[0]

                            # in any other case throw an error
                            elif len(num_ref2) > 1:
                                return (0, 'MAGNITUDE', 'more_magnitude')

                            elif len(num_ref2) == 0:
                                return (0, 'MAGNITUDE', 'no_magnitude')

                        except:
                            return (0, 'MAGNITUDE', 'unknown_error')

            try:
                # Convert both parts to float and add them together to get the final decimal value
                result = float(num1) + float(num2) / (10 ** len(str(num2)))
                return result
            except:
                return (0, 'MAGNITUDE', 'unknown_error')


        else:
            # If input text doesn't match the expected pattern, return None
            return 0

    except:
        return 0


def convert_into_numeric(num_list):
    '''
    This is a function to convert the identified numbers into a numeric form
    '''

    if num_list:

        # at first we examine how many numbers were captured. Only one number should exist
        if len(num_list) > 1:
            return (0, 'MAGNITUDE', 'more_magnitude')

        else:
            target_num = num_list[0]

            # case it is an integer or float, convert it, otherwise move to following cases
            try:

                target_num_float = float(target_num)
                return {'Number': target_num_float}

            except:

                # at first we check for cases like 6,5. If such cases exist we return a format error, otherwise we continue as before
                if ',' in target_num:
                    try:
                        target_num = float(target_num.replace(",", "."))
                        return (0, 'MAGNITUDE', 'format_error')

                    except:
                        return (0, 'MAGNITUDE', 'unknown_error')

                else:

                    # case that it belongs to one of the patterns of freetext number followed by numeric form etc (all the combinations)
                    if "$pattern" in target_num:
                        num, _ = target_num.split("$")

                        # try with this function for all the rest of cases (6 point 5, 6 point five, six point 5)
                        num_conversion = numeric_number_dot_freetext(num)

                        if num_conversion:
                            return {'Number': num_conversion}

                    # if none of the above has worked, then examine the case of freetext numbers without patterns (e.g. two, million, twenty three, etc)
                    else:
                        try:
                            num_conversion = w2n.word_to_num(target_num)
                            return {'Number': num_conversion}

                        # if none of the above try to handle cases of "million and two" or "a million and two". In such cases, we delete any 'a' reference
                        # and we insert the word 'one' at the beginning. In that way the w2n library can handle them besides immediately throw an error
                        except:

                            try:
                                target_num = target_num.replace(" a ", " ")
                                new_target_num = "one " + target_num
                                num_conversion = w2n.word_to_num(new_target_num)
                                return {'Number': num_conversion}

                            except:
                                return (0, 'MAGNITUDE', 'unknown_error')

    else:
        return (0, 'MAGNITUDE', 'no_magnitude')


def magnitude_binding(input_text):
    '''
    This is a function that binds together all the subcomponents of the magnitude number identification, while also controlling for multiple, or zero magnitude references
    '''

    try:

        # capture the referred magnitudes
        target_numbers = capture_numbers(input_text)

        # we only accept for one magnitude reference
        if len(target_numbers) == 1:
            numeric_target_numbers = convert_into_numeric(target_numbers)

            return numeric_target_numbers

        # in case of zero references return the appropriate code (to aid returning the correct prompt)
        elif len(target_numbers) == 0:
            return (0, 'MAGNITUDE', 'no_magnitude')

        # in case of more than one references return the appropriate code (to aid returning the correct prompt)
        elif len(target_numbers) > 1:
            return (0, 'MAGNITUDE', 'more_magnitude')

        # in case of unexpected error return the appropriate code (to aid returning the correct prompt)
        else:
            return (0, 'MAGNITUDE', 'unknown_error')

    except:
        return (0, 'MAGNITUDE', 'unknown_error')


