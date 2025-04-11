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
nlp = spacy.load("en_core_web_lg")


# Define function to compute the average dependency distances from annotated words to the target word
def avg_dependencies_distance(data):
    # 'data' input is what is outputted by the function load_json_files called above

    all_distances = []
    num_files = len(filenames) # get the number of files

    file_distances = []

    for entry in data:
        text = entry['text']
        target_word = entry['word']  # Target word
        labels = entry.get('label', [])  # Handle missing labels
        #labels = entry['label']

        # Process the sentence using spaCy
        doc = nlp(text)


        # Find the target word token
        target_token = None
        for token in doc:
            if token.text == target_word:
                target_token = token
                break

        # If target word is found, calculate distances for labeled words
        if target_token:

            # Get labeled words
            labeled_entities = [label['text'] for label in labels]

            list_labeled_words = [label.split() for label in labeled_entities]
            labeled_words = [word for sublist in list_labeled_words for word in sublist]

            for labeled_word in labeled_words:
                # Find the labeled word token
                labeled_token = None
                for token in doc:
                    if token.text == labeled_word:
                        labeled_token = token
                        break

                # Calculate and print distance if labeled token is found
                if labeled_token:
                    distance = find_distance(target_token, labeled_token, doc)
                    if distance != 0:
                        all_distances.append(distance)

    # Turn the list of all distances into a dictionary with distances and their frequencies
    distance_frequency = Counter(all_distances)

    # Calculate average frequency for each distance
    average_distance_frequency = {distance: count / num_files for distance, count in distance_frequency.items()}

    # Display the chart
    display_dep_freq_chart(average_distance_frequency)


    print(f"Distances for all files {all_distances}")


# Define function to specifically calculate the distances between annotated words and target word
def find_distance(word1, word2, doc):

  """Calculate distance in the dependency tree."""

  # Create a mapping of token index to its head (parent) index
  token_to_head = {token.i: token.head.i for token in doc}

  # Function to find the path from a word to the root
  def get_path_to_root(token_idx):
      path = []
      while token_idx != token_to_head[token_idx]:
          path.append(token_idx)
          token_idx = token_to_head[token_idx]
      path.append(token_idx)
      return path

  # Get the paths from both words to the root
  path1 = get_path_to_root(word1.i)
  path2 = get_path_to_root(word2.i)

  # Find the common ancestor
  common_ancestor = None
  for token in path1:
      if token in path2:
          common_ancestor = token
          break

  # Calculate distance only if common ancestor is found in both paths
  if common_ancestor in path1 and common_ancestor in path2:
      distance = path1.index(common_ancestor) + path2.index(common_ancestor)
      return distance
      #distances[token] = distance
  else:
      # Handle case where common ancestor is not found (e.g., return -1 or None)
      return None  # or None, depending on how you want to handle this case



# PLOT the distances and frequencies
def display_dep_freq_chart(distance_frequency):
    # Filter out 0 and None from labels and values
    filtered_labels = [label for label in distance_frequency if label and label != 0] # Filters out None values & 0s from labels
    filtered_values = [distance_frequency[label] for label in filtered_labels]

    # Generate colors from a colormap
    colors = plt.cm.viridis(np.linspace(0, 1, len(filtered_labels)))

    # Plotting with filtered data and adjusted x-axis
    plt.figure(figsize=(10, 6))
    plt.bar(filtered_labels, filtered_values, color=colors)
    plt.title(f"Average Dependency Distances & Frequencies", fontdict={'family': 'serif'})
    plt.xlabel("Dependency Distance from Trigger Word to Seed Word", fontdict={'family': 'serif'})
    plt.ylabel("Labelled Frequency", fontdict={'family': 'serif'})

    # Start x-axis at 1, and add ticks in steps of 1
    plt.xticks(range(min(filtered_labels), max(filtered_labels)+1, 1))  # Set x-ticks to start at 1 and increment by 1

    plt.show()

    plt.savefig(f"Average_Dependency_Distances.png")



# Run the function to compute dependency distances for each file
# (make sure the filenames are described at start of script)
avg_dependencies_distance(data)