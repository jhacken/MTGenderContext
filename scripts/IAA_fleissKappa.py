# Make sure you have the following installed:
# pip install statsmodels

import pandas as pd
import numpy as np
from ast import literal_eval
import statsmodels.stats.inter_rater
import statsmodels.stats.inter_rater as inter_rater
from statsmodels.stats.inter_rater import fleiss_kappa
from statsmodels.stats.inter_rater import aggregate_raters
from collections import defaultdict
#from nltk.metrics.agreement import AnnotationTask
from utils import load_json_files

# Define list of filenames of all 21 annotators
filenames = ["000", "001", "002", "003", "004", "005", "006", "007", "008", "009",
             "010", "011", "012", "013", "014", "016", "018", "019", "020", "024", "026"]


# Load data from the specified files
data = load_json_files(filenames)


# Define function to calculate Fleiss Kappa between annotators
# The function prints each IAA value between each pair and a total average
def calculate_fleiss_kappa(data):
    # Create a dictionary to store annotations, but with both text and word as keys
    annotations = defaultdict(list)

    # Process the data and extract annotations
    for entry in data:
        text = entry['text']
        word = entry['word']
        annotator = entry['filename']

        if 'label' in entry and entry['label']:
            seen_words_in_sentence = set()

            for label in entry['label']:
                annotated_text = label['text']
                annotated_text = annotated_text.strip()
                annotated_text = annotated_text.strip('!#$%&"()*+,-./:;<=>?@[\]^_`{|}~')

                if word in annotated_text.split() and word not in seen_words_in_sentence:  # Check if word is in annotated text and hasn't been added for this sentence
                    seen_words_in_sentence.add(word)  # Mark word as seen for this sentence
                    label_tags = label['labels']
                    annotations[(text, word)].append((annotator, text, label_tags[0])) # assumes 1 label only

                # Check if any of the target phrases are present
                if any(phrase in annotated_text.split() for phrase in ["construction worker", "construction", "worker"]) and word not in seen_words_in_sentence:
                    seen_words_in_sentence.add(word)
                    label_tags = label['labels']
                    annotations[(text, word)].append((annotator, text, label_tags[0]))

                if any(phrase in annotated_text.split() for phrase in ["Flight attendant", "Flight", "attendant"]) and word not in seen_words_in_sentence:
                    seen_words_in_sentence.add(word)
                    label_tags = label['labels']
                    annotations[(text, word)].append((annotator, text, label_tags[0]))


    # Restructure the data for Fleiss' kappa
    rater_data = []
    for (text, word), text_annotations in annotations.items():
        if len(text_annotations) >= len(filenames):  # Check for equal number of annotations on same (text, word)
            # Create a list of ratings for this item (text, word)
            ratings = [annotation[2] for annotation in text_annotations]  # Extract labels
            rater_data.append(ratings)
        else:
            print(f"Word: {word}, Unequal text annotations: {text_annotations} \n")

    # Convert the data to a NumPy array format suitable for Fleiss' kappa
    # Assuming you have a list of unique categories (labels)
    unique_categories = list(set([rating for sublist in rater_data for rating in sublist]))
    category_mapping = {category: i for i, category in enumerate(unique_categories)}

    # Create a contingency table (NumPy array)
    contingency_table = np.zeros((len(rater_data), len(unique_categories)), dtype=int)
    for i, ratings in enumerate(rater_data):
        for rating in ratings:
            contingency_table[i, category_mapping[rating]] += 1

    # Calculate Fleiss' kappa
    fleiss_kappa_value = inter_rater.fleiss_kappa(contingency_table)
    print(f"All annotators Fleiss kappa: {fleiss_kappa_value}")


# Run the function to calculate IAA for each pair
# (make sure the filenames are described at start of script)
calculate_fleiss_kappa(data)