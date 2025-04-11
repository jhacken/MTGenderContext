# Ensure the following are installed:
# pip install spacy
# python -m spacy download en_core_web_lg

from utils import load_json_files

# Define list of filenames of all 21 annotators
filenames = ["000", "001", "002", "003", "004", "005", "006", "007", "008", "009",
             "010", "011", "012", "013", "014", "016", "018", "019", "020", "024", "026"]


# Load data from the specified files
data = load_json_files(filenames)



# Define function to process and extract raw annotations
def extract_annotations(data):
    # 'data' input is what is outputted by the function load_json_files called above
    for entry in data:
        # text is a sentence (there is a total of 60 annotated sentences)
        text = entry['text']
        word = entry['word']
        filename = entry['filename']

        print(f"Filename: {filename}")
        print(f"Text: {text}")
        print(f"Word: {word}")

        # Check if annotation label exists and is not empty
        if 'label' in entry and entry['label']:
            print("Annotations:")
            for label in entry['label']:
                annotated_text = label['text']
                start = label['start']
                end = label['end']
                label_tags = label['labels'] # male, female, or N/A
                print(f"  - Annotated Text: '{annotated_text}' (from {start} to {end}) with labels: {label_tags}")
        else:
            print("No annotations for this entry.")

        print("\n" + "="*50 + "\n")



# Run function to extract and display the annotations 
# (make sure the filenames are also defined at start)
extract_annotations(data)