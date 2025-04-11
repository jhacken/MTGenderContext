# Make sure you have the following installed:
# pip install nltk==3.8.1
# pip install scikit-learn

import pandas as pd
from ast import literal_eval
from statistics import mean
from sklearn.metrics import cohen_kappa_score
from nltk.metrics.agreement import AnnotationTask
from collections import defaultdict
from itertools import combinations
from utils import load_json_files


# Define list of filenames of all 21 annotators
filenames = ["000", "001", "002", "003", "004", "005", "006", "007", "008", "009",
             "010", "011", "012", "013", "014", "016", "018", "019", "020", "024", "026"]


# Load data from the specified files
data = load_json_files(filenames)


# Define function to calculate Cohens Kappa between annotators and the MT
# The function prints each IAA value between each pair and a total average
def calculate_cohensKappa_with_MT(data):
    # 'data' input is what is outputted by the function load_json_files called above

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

    # Convert annotations to list of tuples
    annotation_data = []
    for (text, word), text_annotations in annotations.items():
        #if len(text_annotations) >= len(filenames): # Check for equal number of annotations on same (text, word)
        annotation_data.extend(text_annotations)
        #else:
        #  print(f"Word: {word}, Unequal text annotations: {text_annotations} \n")

    print(f"Number of sentences compared: {len(annotation_data)/2} \n")


    sentence1 = 'From bookkeeper to ski instructor.'
    sentence2 = 'I cant even deal with this, one follower wrote alongside two fire emojis, while another wrote: "Love the hair x."'

    # Store pairwise Kappas in a dictionary
    pairwise_kappas = {}

    # Calculate and print pairwise agreement
    for annotator1, annotator2 in combinations(filenames, 2):
        if annotator2 == "MT":

            skip_sentences = {"016": sentence1, "010": sentence2}
            # Filter data for the current pair of annotators
            if annotator1 in skip_sentences.keys():
                pairwise_data = [item for item in annotation_data if item[0] in (annotator1, annotator2) and item[1] != skip_sentences[annotator1]]

            else:

                pairwise_data = [item for item in annotation_data if item[0] in (annotator1, annotator2)]

            # Create AnnotationTask object for the pair
            pairwise_task = AnnotationTask(data=pairwise_data)

            # Calculate pairwise agreement
            pairwise_kappa = pairwise_task.kappa()

            # Store pairwise Kappa in the dictionary
            pairwise_kappas[(annotator1, annotator2)] = pairwise_kappa

            # Print pairwise agreement
            print(f"Pairwise Cohen's Kappa ({annotator1}, {annotator2}): {pairwise_kappa}")

            overall_kappas = sum(pairwise_kappas.values()) / len(pairwise_kappas)

    print(f"\nOverall Cohen's Kappa for all annotator-MT: {overall_kappas}")

    # Find and print the maximum and minimum pairwise agreement
    max_kappa = max(pairwise_kappas.values())
    min_kappa = min(pairwise_kappas.values())

    max_pair = [pair for pair, kappa in pairwise_kappas.items() if kappa == max_kappa][0]
    min_pair = [pair for pair, kappa in pairwise_kappas.items() if kappa == min_kappa][0]

    print(f"\nMaximum Pairwise Agreement: {max_kappa} (between {max_pair[0]} and {max_pair[1]})")
    print(f"Minimum Pairwise Agreement: {min_kappa} (between {min_pair[0]} and {min_pair[1]})")



# Run the function to calculate IAA for each pair
# (make sure the filenames are described at start of script)
calculate_cohensKappa_with_MT(data)