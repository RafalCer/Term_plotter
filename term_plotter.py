import os
import json
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md

# Locating default directory for Speeches
current_dir = os.getcwd()
speech_dir_default = current_dir + '/us_presidential_speeches'

# Arguments parsing: terms, parth, title, output
parser = argparse.ArgumentParser()
parser.add_argument('terms', type=str, nargs='*', help='Terms to compare')
parser.add_argument('--path', type=str, nargs='?', default=speech_dir_default,
                    help='Path to the json files')
parser.add_argument('--title', type=str, help='Title of the plot', default='')
parser.add_argument('--output', type=str, help='Title of the output file',\
                    default='')
args = parser.parse_args()

# Assesing that no more than 5 terms are inputted at once
args.terms = [term.lower() for term in args.terms]
if len(args.terms) > 5:
    print('Please provide no more than five terms at once.')
    quit()


''' locating the directory with Speeches'''
if args.path == speech_dir_default:
    # Default directory or no directory inputted
    speeches = os.listdir(args.path)
    # Names of files with speeches
    speech_dir = speech_dir_default
    # Directory with speeches
    
else:
    speech_dir = args.path
    # Non-default directory
    try:
        os.chdir(args.path)
        speeches = os.listdir()
        # Locating and recording the names of the files with speeches
        print('''
          Path recognized.
          NOTE: The graph will be saved in the entered directory (--path).''')
          # Confirmation message
    except FileNotFoundError:
        try:
            if "/" in args.path:
                speech_dir = args.path.replace("/", "\\")
            os.chdir(speech_dir)
            speeches = os.listdir(speech_dir)
            print('''
            Path recognized.
            NOTE: The graph will be saved in the entered directory (--path).''')
            # Simple workaround to avoid errors involving forward\backward slash
        except FileNotFoundError:
            print(f'''
    
    The path you entered, {speech_dir}, does not lead to a valid directory or
    contains no speeches.
    Returning back to the default directory.
    
    
    DEFAULT DIRECTORY:
    {speech_dir_default}...''')
    
        speeches = os.listdir(speech_dir_default)
        speech_dir = speech_dir_default
        # Workaround for invalid speech directories
    
if not args.output:
    # When no name of the outputted graph is given
    args.output = "_".join(args.terms)
    # The name of the ouputted graph will consist of connected terms

data_dictionary = dict()
data_dictionary['speeches'] = list()
data_dictionary['dates'] = list()
data_dictionary['scores'] = list()
data_dictionary['terms'] = list()
# Dictonary to store information about the speeches
no_hits = True
# Boolean to 

for speech_file in speeches:
    if speech_file.endswith('.json'):
        with open(speech_dir + '/' + speech_file, 'r') as infile:
            speech = json.load(infile)
            # Reading in the Speech file
            if speech["Speech"]:
                # If the Speech file contains an actual speech
                data_dictionary['speeches'].append(speech["Speech"].lower())
                # Lowercasing
                initial_date = datetime.datetime.strptime(speech["Date"], "%B %d, %Y")
                # Reading in the date
                converted_date = initial_date.strftime("%Y-%m-%d")
                # Changing the format of the date
                data_dictionary['dates'].append(converted_date)
                # Storing the date of the speech
            else:
                continue
                # For cases when Speech files contain no actual speeches

extracted_dates = data_dictionary['dates'].copy()

vectorizer = TfidfVectorizer(use_idf=True, ngram_range=(1,3),\
                                    stop_words='english')
# Initializing a TfidfVecotizer
matrix = vectorizer.fit_transform(data_dictionary['speeches'])
# Populating a matrix with the vectorized speeches
vocabulary = vectorizer.vocabulary_
# All the words used in the vocabulary and their indices

for term_index, term in enumerate(args.terms):
    # Iterating through the searched terms
    if term in vocabulary:
        if term_index: 
            data_dictionary['dates'].extend(extracted_dates)
            # Adding the date of the Speech if the term is found there
        for speech_index, speech in enumerate(data_dictionary['speeches']):
            # Iterating through the extracted speeches
            if term in speech:
                no_hits = False
                # At least one hit
                term_index = vocabulary[term]
                # Accessing the location of the term in the matrix
                data_dictionary['scores'].append(matrix[speech_index, term_index])
                # Appending the relevancy scores to the dictionary
                data_dictionary['terms'].append(term)
                # Appending the processed term
            else:
                data_dictionary['scores'].append(0)
                # Term not used in speech, thus score is 0
                data_dictionary['terms'].append(term)
                # Appending the processed term
    else:
        print(f'The term {term} has zero hits in the speeches.')


if no_hits:
    # Neither term has hits in the Speeches
    print('''
         =============================================================
         = Neither of the term(s) is used in either of the speeches. =
         = No graph will be printed.                                 =
         =============================================================
         ''')
         
else:
    # At least one term appears in the Speeches at least once
    
    df = pd.DataFrame.from_dict({'Date': data_dictionary['dates'],\
                             'Score': data_dictionary['scores'],\
                                 'Term': data_dictionary['terms']})
    # Initializing Pandas DataFrame
        
    'The format of the date is changed for better redibility'
    
    df['Date'] = pd.to_datetime(df['Date'], format = "%Y-%m-%d")
    fig, ax = plt.subplots(figsize =(15, 7))
    sns.lineplot(ax=ax, x='Date', y='Score', hue='Term',\
                  data=df).set_title(args.title)
    
    'The X axis (years) is set to 35 to avoid cluttering on the graph'
    ax.xaxis.set_major_locator(md.YearLocator(35))
    ax.xaxis.set_major_formatter(md.DateFormatter('%Y'))
    ax.xaxis.set_minor_locator(md.YearLocator(1))
    
    
    plt.savefig(f'{args.output}.png')
    plt.show()
