import spacy
import re
import nltk
from nltk.corpus import wordnet
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

# use spacy small because in that way we are closer to a BOW model which is the one we care in our case since we just compare words
nlp_comparatives = spacy.load('en_core_web_sm', disable=["parser", "ner"])


def find_comptives_symbols(sentence):
    """
    Capture unique cases of symbols like <, >, =, <=, >= and ==
    If more than one symbol exists, return []
    """

    # symbols regex pattern
    pattern = r"(?<![<=>])<=|>=|==|(?<![<=>])<|>|(?<!<)=|=(?![<=>])"

    matches = re.findall(pattern, sentence)

    found_symbols = []
    for matching in matches:
        found_symbols.append({'comparative': matching})

    return found_symbols


def find_comptives_straight_patterns(sentence):
    """
    Function to identivy mentions of comparatives. The form is "comparative adverbs/adjectives followed by than", "words like more/less followed by than", "equal to"
    """

    doc = nlp_comparatives(sentence)
    comparatives = []

    for token in doc:

        # find mentions of "equal" followed by "to"
        if token.text.lower() == "equal":

            next_token = token.nbor()

            if next_token.text.lower() == "to":

                prev_token = token.nbor(-1)

                if prev_token.pos_ == "NOUN":

                    comparatives.append({'comparative': "="})

        # find mentions of "more"/"less" followed by "than"
        elif token.text.lower() in ["more", "less"]:

            next_token = token.nbor()

            if next_token.text.lower() == "than":

                prev_token = token.nbor(-1)

                if token.text.lower() == 'more':

                    comparatives.append({'comparative': '>'})

                elif token.text.lower() == 'less':

                    comparatives.append({'comparative': '<'})

        # find mentions of comparative adjectives or comparative adverbs followed by "than"
        elif token.tag_ == "JJR" or token.tag_ == "RBR":

            next_token = token.nbor()

            if next_token.text.lower() == "than" and next_token.nbor().pos_ != "NOUN":

                # check if the token is a synonym of "bigger"

                # retrieve a set of synonyms for the concepts of 'big' and 'bigger'
                big_synonyms = set(wordnet.synsets('big') + wordnet.synsets('large') + wordnet.synsets('great') + wordnet.synsets('huge') + wordnet.synsets('enormous') + wordnet.synsets('heavy') + wordnet.synsets(
                        'strong') + wordnet.synsets('enormous') + wordnet.synsets('massive') + wordnet.synsets(
                        'immense') + wordnet.synsets('substantial'))
                bigger_synonyms = set(wordnet.synsets('bigger') + wordnet.synsets('larger') + wordnet.synsets(
                    'greater') + wordnet.synsets('higher') + wordnet.synsets('taller') + wordnet.synsets(
                    'heavier') + wordnet.synsets('stronger'))

                bigger_related_words = big_synonyms.union(bigger_synonyms)

                bigger_rel_words = [word.name().split('.')[0] for word in bigger_related_words]

                flag_bigger = 0

                if token.text.lower() in bigger_rel_words:

                    flag_bigger = 1
                    comparatives.append({'comparative': '>'})

                # if no synonym of bigger was found, check for smaller synsets
                if flag_bigger==0:

                    # retrieve a set of synonyms for the concepts of 'small' and 'smaller'
                    small_synonyms = set(wordnet.synsets('small') + wordnet.synsets('little') + wordnet.synsets(
                        'tiny') + wordnet.synsets('petite') + wordnet.synsets('miniature') + wordnet.synsets(
                        'slight') + wordnet.synsets('meager') + wordnet.synsets('inconsequential') + wordnet.synsets(
                        'minor'))
                    smaller_synonyms = set(wordnet.synsets('smaller') + wordnet.synsets('lesser') + wordnet.synsets(
                        'lower') + wordnet.synsets('shorter') + wordnet.synsets('lighter') + wordnet.synsets('weaker'))

                    smaller_related_words = small_synonyms.union(smaller_synonyms)
                    smaller_rel_words = [word.name().split('.')[0] for word in smaller_related_words]

                    if token.text.lower() in smaller_rel_words:

                        flag_bigger = 0
                        comparatives.append({'comparative': '<'})

    return comparatives


# helper functions for 'identify_pattern_bigger_smaller'
def identify_comparison(sentence):
    """
    Capture patterns of 'word-er' followed by 'than' (e.g. 'better than', 'lesser than', etc)
    """

    pattern = r'\b(\w+er than)\b'
    matches = re.findall(pattern, sentence)

    if matches:
        return matches
    else:
        return 0


def find_more_than_reference(sentence):
    """
    Capture patterns of 'more' followed by 'word' followed by 'than' (e.g. more advanced than)
    """

    pattern = r"(more) (\w+) than"
    matches = re.findall(pattern, sentence)

    if matches:
        return [' '.join(match) for match in matches]
    else:
        return 0


def find_less_than_reference(sentence):
    """
    Capture patterns of 'less' followed by 'word' followed by 'than' (e.g. less advanced than)
    """

    pattern = r"(less) (\w+) than"
    matches = re.findall(pattern, sentence)

    if matches:
        return [' '.join(match) for match in matches]
    else:
        return 0


def is_related_to(word, target_word):
    """
    Returns True if the input 'word' is semantically related to the 'target_word', otherwise False.
    """

    target_synsets = set(wordnet.synsets(target_word))
    word_synsets = set(wordnet.synsets(word))

    if word_synsets.intersection(target_synsets):
        return True
    else:
        return False


def is_related_to_bigger(word):
    """
    Returns True if the input 'word' is semantically related to the concept 'bigger', otherwise False.
    """

    if word.lower() == "more" or word.lower().startswith("more "):
        return True

    # retrieve a set of synonyms for the concepts of 'big' and 'bigger'
    big_synonyms = set(wordnet.synsets('big') + wordnet.synsets('large') + wordnet.synsets('great') + wordnet.synsets(
        'huge') + wordnet.synsets('enormous') + wordnet.synsets('heavy') + wordnet.synsets('strong') + wordnet.synsets(
        'enormous') + wordnet.synsets('massive') + wordnet.synsets('immense') + wordnet.synsets('substantial'))
    bigger_synonyms = set(
        wordnet.synsets('bigger') + wordnet.synsets('larger') + wordnet.synsets('greater') + wordnet.synsets(
            'higher') + wordnet.synsets('taller') + wordnet.synsets('heavier') + wordnet.synsets('stronger'))

    related_words = big_synonyms.union(bigger_synonyms)

    # Check if the input word is semantically related to any of those 'big'/'bigger' synonyms
    for related_word in related_words:
        if is_related_to(word, related_word.name().split('.')[0]):
            return True
    return False


def is_related_to_smaller(word):
    """
    Returns True if the input word is semantically related to the concept of 'smaller', otherwise False.
    """
    if word.lower() == "less" or word.lower().startswith("less "):
        return True

    # retrieve a set of synonyms for the concepts of 'small' and 'smaller'
    small_synonyms = set(
        wordnet.synsets('small') + wordnet.synsets('little') + wordnet.synsets('tiny') + wordnet.synsets(
            'petite') + wordnet.synsets('miniature') + wordnet.synsets('slight') + wordnet.synsets(
            'meager') + wordnet.synsets('inconsequential') + wordnet.synsets('minor'))
    smaller_synonyms = set(
        wordnet.synsets('smaller') + wordnet.synsets('lesser') + wordnet.synsets('lower') + wordnet.synsets(
            'shorter') + wordnet.synsets('lighter') + wordnet.synsets('weaker'))

    related_words = small_synonyms.union(smaller_synonyms)

    # Check if the input word is semantically related to any of those 'small'/'smaller' synonyms
    for related_word in related_words:
        if is_related_to(word, related_word.name().split('.')[0]):
            return True
    return False


def identify_bigger_smaller_advanced(sentence):
    """
    This is a complementary function to capture cases of 'words ending with -er' followed by 'than' and cases of 'more'/'less' followed 'word' followed by 'than'
    """

    # pattern 'words ending with -er' followed by 'than' (pattern1)
    word_er_than = identify_comparison(sentence)

    # pattern 'more' followed 'word' followed by 'than' (pattern2)
    more_word_than = find_more_than_reference(sentence)

    # pattern 'less' followed 'word' followed by 'than' (pattern3)
    less_word_than = find_less_than_reference(sentence)

    bigger_list = []
    smaller_list = []

    # in case any pattern is captured
    if word_er_than or more_word_than or less_word_than:

        # in case of pattern1
        if word_er_than:
            for word in word_er_than:

                # perform relevant substitutions
                target_word = word.replace("than", "").strip()

                # examine if it is a bigger-related or smaller-related word
                bigger_word = is_related_to_bigger(target_word)
                smaller_word = is_related_to_smaller(target_word)

                # case of bigger word
                if bigger_word and not smaller_word:
                    bigger_list.append({"comparative": ">"})

                # case of smaller word
                elif smaller_word and not bigger_word:
                    smaller_list.append({"comparative": "<"})

        # in case of pattern2
        if more_word_than:
            for word in more_word_than:

                # perform relevant substitutions
                target_word = word.replace("than", "").replace("more", "").strip()

                # in this case it must be a bigger-related word
                bigger_word = is_related_to_bigger(target_word)

                # case of bigger word
                if bigger_word:
                    bigger_list.append({"comparative": ">"})

        # in case of pattern3
        if less_word_than:
            for word in less_word_than:

                # perform relevant substitutions
                target_word = word.replace("than", "").replace("less", "").strip()

                # in this case it must be a lesser-related word
                lesser_word = is_related_to_smaller(target_word)

                # case of bigger word
                if lesser_word:
                    smaller_list.append({"comparative": "<"})

    # return the combined list
    return bigger_list + smaller_list


def find_equal_to_comptives_ngrams(sentence):
    """
    This function takes a sentence as input and returns a reference phrase based on semantic similarity using n-grams.
    The possible reference phrases are provided as a list.
    """

    # This is a reference list for the concept of 'equal to'. It has many references to perform on them the semantic similarity examination
    possible_references = ["equal to", "same as", "similar to", "identical to", "equivalent to", "tantamount to",
                           "corresponding to", "comparable to", "akin to", "commensurate with", "in line with",
                           "on a par with", "indistinguishable from", "corresponding with", "congruent with"]

    # that thershold is enough empirically
    max_similarity = 0.85

    possible_reference_list = []

    # parse with the spacy model (embeddings each of the references)
    embedding_references = []
    for reference in possible_references:
        reference_doc = nlp_comparatives(reference)
        embedding_references.append(reference_doc)

    # Check 2-grams, 3-grams, and 4-grams
    for n in range(2, 5):

        # get n-grams
        sentence_ngrams = list(nltk.ngrams(sentence.split(), n))

        for sent_ngram in sentence_ngrams:
            sentence_ngram_str = ' '.join(sent_ngram)
            sentence_ngram_doc = nlp_comparatives(sentence_ngram_str)

            for emb_ref in embedding_references:
                similarity = sentence_ngram_doc.similarity(emb_ref)

                if similarity >= max_similarity:
                    possible_reference_list.append({'comparative': "="})
                    break

    # if we have found a possible refernce that is similar enough with an n-gram of the input sentence, return the comparative '=', otherwise return 0
    if possible_reference_list:
        return possible_reference_list
    else:
        return []


def single_verb_comptives(sentence):
    """
    This function takes a sentence and identifies any mention of bigger than, smaller than, equal to, expressed
    as single-word verb. It uses wordnet synsets to examine for synonyms and antonyms
    """

    # base references
    bigger_references_sg = ["surpass", "exceed", "outstrip", "outdo", "outrank", "transcend"]
        lesser_references_sg = ["subside", "depreciate", "curtail"]
    equal_references_sg = ["match", "equal", "agree", "comply"]

    doc = nlp_comparatives(sentence)

    bigger_list = []
    smaller_list = []
    equal_list = []

    # search for all verbs and examine their lemma with all the synonyms of each of the previous references. Assign a label accordingly
    for token in doc:

        # first examine for 1-1 pair matching and 1-1 lemma pair matching
        if token.text in bigger_references_sg or token.lemma_ in bigger_references_sg:
            bigger_list.append({'comparative': ">"})
            break

        elif token.text in lesser_references_sg or token.lemma_ in lesser_references_sg:
            smaller_list.append({'comparative': "<"})
            break

        elif token.text in equal_references_sg or token.lemma_ in equal_references_sg:
            equal_list.append({'comparative': "="})
            break

        else:

            # if not, then try with synonyms only for verbs
            if token.pos_ == "VERB":

                for lemma in token.lemma_.split('|'):
                    synsets = wordnet.synsets(lemma, pos='v')

                    for syn in synsets:
                        if any(lemma in bigger_references_sg for lemma in syn.lemma_names()):
                            bigger_list.append({'comparative': ">"})
                            break

                        elif any(lemma in lesser_references_sg for lemma in syn.lemma_names()):
                            smaller_list.append({'comparative': "<"})
                            break

                        elif any(lemma in equal_references_sg for lemma in syn.lemma_names()):
                            equal_list.append({'comparative': "="})
                            break

    final_list = bigger_list + smaller_list + equal_list

    if final_list:
        return final_list
    else:
        return []


# helper functions for 'identify_multi_word_verbs'

# Define multi-word verb lists
bigger_list = ["is a cut above", "is ahead of", "is superior to", "is greater than", "is a class apart"]
smaller_list = ["fall behind", "is inferior to", "is smaller than", "lag behind", "trail behind", "fall short", "fall beneath"]
equal_list = ["is in line with", "is equal to", "is on a par with", "is the same as", "is comparable to", "is in sync with", "is in harmony with", "is in step with", "is in tune with", "is in accord with", "is consistent with", "is consonant with", "is equivalent to"]

# Calculate embeddings of multi-word verbs
bigger_embeddings = [np.mean([token.vector for token in nlp_comparatives(verb)], axis=0) for verb in bigger_list]
smaller_embeddings = [np.mean([token.vector for token in nlp_comparatives(verb)], axis=0) for verb in smaller_list]
equal_embeddings = [np.mean([token.vector for token in nlp_comparatives(verb)], axis=0) for verb in equal_list]


# Define function to check if n-gram is in multi-word verb list
def check_list(ngram, verb_list):
    """
    This is a function to check if n-gram is in multi-word verb list
    """

    if ngram in verb_list:
        return True
    else:
        return False


def cosine_sim(a, b):
    """
    This is a function to calculate cosine similarity
    """

    return cosine_similarity(a.reshape(1,-1), b.reshape(1,-1))[0][0]


# we examine the n-grams reversely and any time we find a match, we "delete" that match, so that lesser ngrams will not be matched \
# (e.g. is on a par with, would also match afterwords on a par with, par with, etc)

def multiword_verb_comptives(sentence):
    """
    This function takes a sentence and identifies any mention of bigger than, smaller than, equal to, expressed
    as multi-word verbs. Based on three refernces lists it performs initially a simple string comparison with each
    of their elements and the ngrams of the input sentence. If there is no match there, it performs the same procedure
    with cosine similarity to identify any similar ngrams.
    """

    # Split sentence into tokens
    tokens = sentence.split()

    # Initialize variables to store label and max similarity
    label = None
    max_sim = 0

    # these lists are used to capture any possible reference
    bigger_l = []
    smaller_l = []
    equal_l = []

    # Define set to keep track of matched ngrams
    matched_ngrams = set()

    # Iterate through n-grams of sentence, starting with the largest n-grams
    for n in range(5, 0, -1):
        for i in range(len(tokens)-n+1):
            ngram = ' '.join(tokens[i:i+n])

            # Skip ngrams that have already been matched
            if ngram in matched_ngrams:
                continue

            # Check if n-gram is in bigger_list
            if check_list(ngram, bigger_list):
                matched_ngrams.update(set(ngram.split()))
                bigger_l.append({"comparative": '>'})

            # Check if n-gram is in smaller_list
            elif check_list(ngram, smaller_list):
                matched_ngrams.update(set(ngram.split()))
                smaller_l.append({"comparative":'<'})

            # Check if n-gram is in equal_list
            elif check_list(ngram, equal_list):
                matched_ngrams.update(set(ngram.split()))
                equal_l.append({"comparative": '='})

            # Check if n-gram is similar to any verb in bigger_list using pre-calculated embeddings
            else:
                ngram_emb = np.mean([token.vector for token in nlp_comparatives(ngram)], axis=0)
                similarities_bigger = [cosine_sim(ngram_emb, verb_emb) for verb_emb in bigger_embeddings]
                max_sim_bigger = max(similarities_bigger)

                # Check if n-gram is similar to any verb in smaller_list using pre-calculated embeddings
                similarities_smaller = [cosine_sim(ngram_emb, verb_emb) for verb_emb in smaller_embeddings]
                max_sim_smaller = max(similarities_smaller)

                # Check if n-gram is similar to any verb in equal_list using pre-calculated embeddings
                similarities_equal = [cosine_sim(ngram_emb, verb_emb) for verb_emb in equal_embeddings]
                max_sim_equal = max(similarities_equal)

                # Determine the maximum similarity value among the three lists
                if max_sim_bigger > max_sim_smaller and max_sim_bigger > max_sim_equal and max_sim_bigger > max_sim:
                    max_sim = max_sim_bigger
                    if max_sim > 0.9:
                        matched_ngrams.update(set(ngram.split()))
                        bigger_l.append({"comparative":'>'})
                    else:
                        matched_ngrams.update(set(ngram.split()))


                elif max_sim_smaller > max_sim_bigger and max_sim_smaller > max_sim_equal and max_sim_smaller > max_sim:
                    max_sim = max_sim_smaller
                    if max_sim > 0.9:
                        matched_ngrams.update(set(ngram.split()))
                        smaller_l.append({"comparative":'<'})
                    else:
                        matched_ngrams.update(set(ngram.split()))


                elif max_sim_equal > max_sim_bigger and max_sim_equal > max_sim_smaller and max_sim_equal > max_sim:
                    max_sim = max_sim_smaller
                    if max_sim > 0.9:
                        matched_ngrams.update(set(ngram.split()))
                        equal_l.append({"comparative":'='})
                    else:
                        matched_ngrams.update(set(ngram.split()))


    return bigger_l + smaller_l + equal_l


def identify_double_symbol_comparisons(sentence):
    """
    Identifies comparison phrases in a given sentence.
    Returns a list of matched phrases and their corresponding operators.
    """

    comparison_phrases = [
        ["less than or equal to", "less or equal to", "smaller than or equal to",
         "smaller or equal to", "lower than or equal to", "lower or equal to",
         "inferior to or equal to", "inferior or equal to", "lesser or equal to"],
        ["greater than or equal to", "greater or equal to", "more than or equal to",
         "more or equal to", "higher than or equal to", "higher or equal to",
         "above than or equal to", "above or equal to", "larger than or equal to",
         "larger or equal to", "superior to or equal to", "superior or equal to",
         "bigger or equal to", "over or equal to", "surpassing or equal to"]
    ]

    operators = {
        "less than or equal to": "<=",
        "less or equal to": "<=",
        "smaller than or equal to": "<=",
        "smaller or equal to": "<=",
        "lower than or equal to": "<=",
        "lower or equal to": "<=",
        "inferior to or equal to": "<=",
        "inferior or equal to": "<=",
        "greater than or equal to": ">=",
        "greater or equal to": ">=",
        "more than or equal to": ">=",
        "more or equal to": ">=",
        "higher than or equal to": ">=",
        "higher or equal to": ">=",
        "above than or equal to": ">=",
        "above or equal to": ">=",
        "larger than or equal to": ">=",
        "larger or equal to": ">=",
        "superior to or equal to": ">=",
        "superior or equal to": ">=",
        "bigger or equal to": ">=",
        "over or equal to": ">=",
        "lesser or equal to": "<=",
        "surpassing or equal to": ">="
    }

    found_phrases = []
    found_operators = []
    for variations in comparison_phrases:
        pattern = r"\b(" + "|".join([re.escape(v) for v in variations]) + r")\b"
        matches = re.findall(pattern, sentence, re.IGNORECASE)
        if matches:
            for match in matches:
                found_phrases.append(match)
                found_operators.append(operators[match])

    comparative_list = [{'comparative': []}]
    for phrase, operator in zip(found_phrases, found_operators):
        comparative_list[0]['comparative'].append((phrase, operator))

    final_comptives_list = [{'comparative': comparative_list[0]['comparative'][i:i + 2]} for i in range(0, len(comparative_list[0]['comparative']), 2)]

    final_clean_list = []
    for item in final_comptives_list:
        for value in item['comparative']:
            final_clean_list.append({'comparative': value})

    return final_clean_list


def check_substrings(lst):
    """
    This function checks all the elements of a list and if any substring exist in any other element it returns a list of tuples
    where the first element is the substring and the second the string that contains the substring
    """
    substring_tuples = []
    for i, comp1 in enumerate(lst):
        for j, comp2 in enumerate(lst):
            if i == j:
                continue
            if comp1['comparative'][0] in comp2['comparative'][0]:
                substring_tuples.append((comp1, comp2))
    return substring_tuples


def identify_comparatives(sentence):
    """
    This function combines the results of all the aforementioned techniques (simple and advance) to identify bigger than, smaller than, equal to patterns
    """

    # first identify the double symbols (<= >= ==)
    identify_double_symbols_initial = identify_double_symbol_comparisons(sentence)

    # this is because (for example) bigger than is a subset of bigger or equal than (and it returns conflicts)
    if identify_double_symbols_initial:
        for elem in identify_double_symbols_initial:
            sentence = sentence.replace(elem['comparative'][0], " ")

    identify_double_symbols = []

    for item in identify_double_symbols_initial:
        for k, v in item.items():
            if isinstance(v, tuple):
                item[k] = v[1]
        identify_double_symbols.append(item)

    # Identify straightforward patterns
    straight_comptives = find_comptives_straight_patterns(sentence)

    # Identify advanced bigger/smaller comparativesunknown_error
    bigger_smaller_comparatives = identify_bigger_smaller_advanced(sentence)

    # Identify advanced equal-to comparatives
    equal_to_comparatives = find_equal_to_comptives_ngrams(sentence)

    single_verb = single_verb_comptives(sentence)

    multi_verb = multiword_verb_comptives(sentence)

    # return all the patterns that were captured
    comparatives = straight_comptives + bigger_smaller_comparatives + equal_to_comparatives + single_verb + multi_verb + identify_double_symbols

    # since those different techniques might capture similar patterns, we keep only unique references. More precisely
    # we discard any unique reference while also any reference thay may exist as a substring on any other reference

    # sort the list by length of the comparatives, in descending order
    comparatives.sort(key=lambda item: len(item['comparative'][0]), reverse=False)

    unique_comparatives = {}
    for i, item in enumerate(comparatives):
        comparative = item['comparative'][0]
        # check if the comparative is already in the dictionary or a substring/similar string of an existing comparative
        is_unique = True
        for existing_comp in unique_comparatives:
            if (comparative in existing_comp) or (existing_comp in comparative):
                is_unique = False
                break
        if is_unique:
            unique_comparatives[comparative] = item
        elif i == len(comparatives) - 1:
            # if it's the last item and it's not unique, replace the first unique item in the list with this item
            for j, existing_item in enumerate(unique_comparatives.values()):
                if (existing_item['comparative'][0] in comparative) or (comparative in existing_item['comparative'][0]):
                    unique_comparatives.pop(list(unique_comparatives.keys())[j])
                    unique_comparatives[comparative] = item
                    break

    unique_output = list(unique_comparatives.values())

    clean_unique_output = []

    # this snippet is to handle the extra cases of smaller than or equal to etc
    # in case a reference of eg "smaller than" is found by the previous modules, while also a reference of "smaller than or equal to"
    # then the snippet checks whether the "smaller than" reference exists only as a substring of "smaller than or equal to" or if it
    # also exists as a seperate, standalone reference on the initial sentence (in which case it is kept, otherwise it is dismissed)
    if len(unique_output) > 1:
        list_of_tuples = check_substrings(unique_output)

        for elem in list_of_tuples:
            dupl_sent = sentence
            dupl_sent = dupl_sent.replace(elem[1]['comparative'][0], " ")

            clean_unique_output.append(elem[1])

            if elem[0]['comparative'][0] in dupl_sent:
                clean_unique_output.append(elem[0])

    if clean_unique_output:
        return clean_unique_output

    else:
        return unique_output


def comparatives_binding(sentence):
  #
  try:
    comparative_symbols = find_comptives_symbols(sentence)
    comparative_mentions = identify_comparatives(sentence)

    # starting with the symbols, if one was captured
    if len(comparative_symbols) == 1:

      # if the rest of the functions are empty (meaning that there are no other references)
      if len(comparative_mentions) == 0:
        return comparative_symbols[0]

      else:
        return (0, "COMPARATIVES", "more_comparatives_mentions")

    # in case that there is no symbol
    elif len(comparative_symbols) == 0:

      # we need only one mention of comparatives
      if len(comparative_mentions) == 1:
        return comparative_mentions[0]

      # case of no comparative mentions
      elif len(comparative_mentions) == 0:
        return (0, "COMPARATIVES", "no_comparatives")

      # case of no more than one comparative mentions
      else:
        return (0, "COMPARATIVES", "more_comparatives_mentions")

    # case of multiple symbol references
    else:
      return (0, "COMPARATIVES", "more_symbol_comparatives")

  except:
    return (0, "COMPARATIVES", "unknown_error")