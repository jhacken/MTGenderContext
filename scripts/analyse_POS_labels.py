import spacy
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from utils import load_json_files

# Define list of filenames of all 21 annotators
filenames = ["000", "001", "002", "003", "004", "005", "006", "007", "008", "009",
             "010", "011", "012", "013", "014", "016", "018", "019", "020", "024", "026"]

# Load data from the specified files
data = load_json_files(filenames)


# Load spaCy English model
nlp = spacy.load('en_core_web_lg')


# Define function to tag the annotations with POS labels
pos_counts_dic_all = {}

def process_json_with_pos_annotations_all(data):
    # 'data' input is what is outputted by the function load_json_files called above
    file_pos_counts = {}  # Dictionary to store POS counts for each file

    for entry in data:
        if 'label' in entry and entry['label']:
            filename = entry['filename']
            if filename not in file_pos_counts:
                file_pos_counts[filename] = Counter()  # Initialize Counter for the file

            text = entry['text']
            labels = entry['label']
            word = entry['word']

            # Process the sentence using spaCy
            doc = nlp(text)

            for label in labels:
                annotated_text = label['text']
                start = label['start']
                end = label['end']

                if annotated_text.strip() == word:
                  continue  # Skip to the next iteration

                if annotated_text.strip() in ["Flight attendant", "construction", "worker"]: # Specifically skip (not recognised by 'word' above)
                  continue  # Skip to the next iteration

                annotated_word = text[start:end]

                seen_words = set()  # to avoid repetitions
                for token in doc:
                    #if token.text == annotated_word:
                    if (token.text == annotated_text or token.text in annotated_text.split()) and token.text not in seen_words:
                       # print(f"Word: {token.text}, POS: {token.pos_}")
                        seen_words.add(token.text)
                        pos_label = token.pos_
                        file_pos_counts[filename][pos_label] += 1


    # Print POS counts and display charts for each file
    for filename, pos_counts in file_pos_counts.items():
        print(f"\nPOS counts for file {filename}:")
        for pos, count in pos_counts.items():
            print(f"{pos}: {count}")

        # Call function to display POS charts for each file    
        display_pos_chart(pos_counts, filename)

    print(f"POS file: {file_pos_counts}")
    pos_counts_dic_all[filename] = file_pos_counts


# Define function to display POS charts for each file
def display_pos_chart(pos_counts, filename):
    labels = list(pos_counts.keys())
    values = list(pos_counts.values())

    # Sort the data by values in descending order
    sorted_data = sorted(zip(values, labels), reverse=True)
    sorted_values, sorted_labels = zip(*sorted_data)

    # Generate colors from a colormap
    colors = plt.cm.viridis(np.linspace(0, 1, len(labels)))

    plt.figure(figsize=(10, 6))
    plt.bar(sorted_labels, sorted_values, color=colors)
    plt.title(f"Part of Speech Counts for Annotated Words in File {filename}", fontdict={'family': 'serif'})
    plt.xlabel("POS Labels")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.show()

    plt.savefig(f"POS_of_Annotated_Triggers_{filename}.png")



# Run the function to collect POS information for each file
# (make sure the filenames are described at start of script)
process_json_with_pos_annotations_all(data)