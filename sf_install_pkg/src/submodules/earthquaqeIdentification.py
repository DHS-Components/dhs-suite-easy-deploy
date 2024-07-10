import spacy
import numpy as np

# Load the spacy model with GloVe embeddings
nlp = spacy.load("en_core_web_lg")

# Define earthquake-related keywords
earthquake_single_keywords = ['earthquake', 'seismic', 'tremor', 'quake', 'aftershock', 'seismology', 'tectonic', 'plate', 'seismometer', 'temblor', 'trembler', 'seism', 'shock', 'vibration', 'shake', 'groundswell', 'earthquakes', 'seismics', 'tremors', 'quakes', 'aftershocks', 'seismologies', 'tectonics', 'plates', 'seismometers', 'temblors', 'tremblers', 'seisms', 'shocks', 'vibrations', 'shakes', 'groundswells']

# Compute embeddings for single-word keywords
earthquake_single_embeddings = [nlp(keyword).vector for keyword in earthquake_single_keywords]

# Define multi-word earthquake-related keywords
earthquake_multi_keywords = ['seismic activity', 'earthquake risk', 'earthquake zone', 'seismic wave', 'earthquake damage', 'seismic shift', 'tectonic plate', 'fault line', 'seismic retrofitting', 'seismic hazard', 'aftershock sequence', 'earthquake drill', 'seismic reflection', 'plate tectonic', 'seismic tomography', 'seismic profiling', 'seismicity pattern', 'earthquake swarm', 'seismic gap', 'seismic inversion', 'seismic reflection', 'seismic scattering', 'seismic attenuation', 'seismic imaging', 'seismic map', 'seismic data', 'earthquake monitoring', 'earth shaking', 'seismic activities', 'earthquake risks', 'earthquake zones', 'seismic waves', 'earthquake damages', 'seismic shifts', 'tectonic plates', 'fault lines', 'seismic retrofittings', 'seismic hazards', 'aftershock sequences', 'earthquake drills', 'seismic reflections', 'plate tectonics', 'seismic tomographies', 'seismic profilings', 'seismicity patterns', 'earthquake swarms', 'seismic gaps', 'seismic inversions', 'seismic reflections', 'seismic scatterings', 'seismic attenuations', 'seismic imagings', 'seismic maps', 'earth shakings']

# Compute embeddings for multi-word keywords
earthquake_multi_embeddings = []
for keyword in earthquake_multi_keywords:
    keyword_embeddings = [nlp(w).vector for w in keyword.split()]
    combined_emb = np.mean(keyword_embeddings, axis=0)  # Compute the average embedding for the multi-word token
    earthquake_multi_embeddings.append(combined_emb)

def straight_pattern_matching(ngram):
  """
  Function to compute a straightforward similarity between a word and the pre-defined references
  """
  if ngram in earthquake_single_keywords or ngram in earthquake_multi_keywords:
    return ngram
  else:
    return False


# Define a function to compute the semantic similarity between a word and a set of embeddings
def compute_similarity_earthquake(word, embeddings, excluded_keywords):
    """
    Compute the semantic similarity for earthquaqe events
    """

    # Check if the word is in the excluded keywords list
    if word in excluded_keywords:
        return False

    # Compute the GloVe embedding of the word
    word_emb = nlp(word).vector

    # Compute the cosine similarity between the word embedding and the keyword embeddings
    similarity_scores = [np.dot(word_emb, emb) / (np.linalg.norm(word_emb) * np.linalg.norm(emb)) for emb in embeddings]

    # Return if the maximum similarity score is above a certain threshold
    if max(similarity_scores) > 0.7:
      return word

    else:
      return False


def identify_earthquake_event(input_sentence):
    """
    Compute the semantic similarity for earthquaqe events
    """

    try:

        # Define excluded keywords to ignore (because cases like I want bars with magnituted 6 - were given as correct)
        excluded_keywords = ['magnitude', 'richter', 'moment', 'scale', 'intensity', 'amplitude', 'energy', 'force',
                             'power', 'seismicity', 'event',
                             'magnitudes', 'richters', 'moments', 'scales', 'intensities', 'amplitudes', 'energies',
                             'forces', 'powers', 'seismicities', 'events']

        parsed_sentence = nlp(input_sentence)

        # start with simple straight pattern matching of single keywords
        for word in parsed_sentence:
            if word.text not in excluded_keywords:
                straight_matching_single = straight_pattern_matching(word.text)

                if straight_matching_single:
                    # return {'earthquaqe_event': [True, straight_matching_single]}
                    return {"event": "earthquake"}

        # Continue with embeddings single matching
        earthquaqe_keywords_single = []

        # Check for single-word earthquake-related keywords
        earthquaqe_keywords_single = [
            compute_similarity_earthquake(word.text.lower(), earthquake_single_embeddings, excluded_keywords) for word
            in parsed_sentence]

        single_keyword_flag = False

        # check until you find one such reference and then break
        for elem in earthquaqe_keywords_single:
            if elem:
                single_keyword_flag = True
                target_elem_single = elem
                break

        # if there is at least one referece, we can assume that the sentence refers to earthquaqe events
        if single_keyword_flag:
            return {"event":"earthquake"}

        # otherwise we examine for 2grams multi-word straight patterns and embeddings
        earthquaqe_keywords_multi = []

        # check 2-grams
        for i in range(len(parsed_sentence) - 1):
            bigram = parsed_sentence[i:i + 2].text.lower()

            # case of straight matching
            straight_matching_multi = straight_pattern_matching(word.text)

            if straight_matching_multi:
                return {"event": "earthquake"}

            # if no straight matching then perform embeddings
            else:
                earthquaqe_keywords_multi.append(
                    compute_similarity_earthquake(bigram, earthquake_multi_embeddings, excluded_keywords))

        # case that the straight multi matching did not give any output
        multi_keyword_flag = False

        # check until you find one such reference and then break
        for elem in earthquaqe_keywords_multi:
            if elem:
                multi_keyword_flag = True
                target_elem_multi = elem
                break

        # if there is at least one referece, we can assume that the sentence refers to earthquaqe events
        if multi_keyword_flag:
            return {"event":"earthquake"}

        # otherwise there is no reference
        else:
            return (0, 'EARTHQUAKE_EVENT', 'no_earthquake_reference')

    except:
        return (0, 'EARTHQUAKE_EVENT', 'unknown_error')