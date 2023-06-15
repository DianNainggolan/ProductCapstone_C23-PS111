# HEALTH DIARY
## ProductCapstone_C23-PS111

## Description
This Machine Learning Model can be used to predict user mental condition based on user writing.

## Method
Classification with a Recurrent Neural Network that using pre-trained word vectors from [glove](https://nlp.stanford.edu/projects/glove/) and bidirectional lstm layer using Tensorflow 

## TOOLS
- Python
- TensorFlow
- NumPy
- Pandas
- Seaborn
- Matplotlib
- Google Drive
- Google Collab
- Sklearn
- Pickle
- Contractions
- Spacy
- Re
- String
- Random

## HOW TO PREDICT
The model can predict the user mental condition by inputing what user writing

## DOCUMENTATION
The following are the details on how others may replicate our steps:
1. Download the dataset
2. Upload dataset to the notebook
3. Preprocessing data before being used
4. Get sample for the dataset
5. Split the dataset into texts_train, texts_test, labels_train, labels_test
6. Tokenize, sequence and padding texts_train, texts_test, labels_train, labels_test
7. Download pre-trained word vectors from glove and upload to the notebook
8. Load the pre-trained word vectors from glove and Represent the words in your vocabulary using the embeddings
9. Training and validating the model
10. Convert to keras to store the weights and model configuration to .h5 format
11. Save tokenizer that used before using pickle
12. For quote recommendation, combine the quote dataset and the user input. Then using cosine similarity to get the recommendation 
