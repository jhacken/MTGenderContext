# MTGenderContext

This repository is a companion of the paper Gender Bias and the Role of Context in Human Perception and Machine Translation.
This paper investigates human gender bias and its relation to bias in machine translation (MT), focussing on the role of context in gender interpretation. To this end, we measured human implicit gender bias and conducted an annotation study, followed by a linguistic and computational analysis to compare human gender perceptions among themselves and with machine translations. We created a dataset and collected annotations on gender perception of target words in ambiguous contexts and how and which trigger words lead to this perception. The study shows that, unlike MT, humans exhibit highly varied perceptions of gender in ambiguous contexts. A linguistic analysis on annotated trigger words reveals that proper nouns, nouns and adjectives frequently affect human gender perception.

## Content
This repository includes:
- list of ~150 seed words used to filter data, including their gender-inflection (female, male, neutral)
- dataset of 60 gender-ambiguous natural sentences (English)
- German DeepL translations of dataset [to-do]
- manual annotations conducted by 20 annotators
- scripts for annotation anaylsis [to-do]
- scripts for IAA [to-do]
- reference to [scripts for pygamma](https://github.com/TomMoeras/parallel-pygamma), compiled for this paper for a use case of a large number of annotators
