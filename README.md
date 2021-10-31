# Term Plotter

This file contains instructions for the term_plotter.py program. 

## -----Functionality-----
The program outputs a term plot of the tfidf scores of inputted terms in the specified speeches. The outputted graph visualises the prominence of the specified n-grams from a diachronic perspective. Terms that have 0 hits throughout the speeches will not be shown on the graph. Nevertheless, the program will print a statement to notify the user about terms that had 0 hits. 


## -----How to run it-----
To run the code, open the command line (cmd) and start the program by running a command in the following format:

> python3 term_plotter.py "term1" "term2" "term3"... (--path path) (--title title) (--output output).


## -------Arguments ------
There are four arguments:

- 'terms'      -->  A string or a list of strings that specify the terms you would like to    analyse diachronically
- '--path'     -->  An optional string that indicates the path to directory with speeches to be analyzed. The default directory is ./us_presidential_speeches.
- '--title'    -->  An optional string that specifies the preferred title of your graph. No title is shown on the graph is no title is specified.
- '--output'   -->  An optional string whcih specified the preferred name of the file where your graph will be saved. The default name of the file is concatenated terms separated by whitespace. 


## --------Example--------

> python3 term_plotter.py "Live" "Laugh" "Love" --path ./important_quotes --title LLL --output this_is_a_joke

OUTPUT:

(Your graph will be saved in the same directory as the specified path or the current direcotry if the specified path is invalid.)


## --------Get help-------
If you need help, you can run the following:
> python3 term_plotter.py -h


## -------Exceptions-------
1. : The following message will appear if neither of the specified terms appears in the speeches.

         =============================================================
         = Neither of the term(s) is used in either of the speeches. =
         = No graph will be printed                                  =
         =============================================================

2. : If the inputted directory (--path) is invalid, the program switches back to the default dir:
 ./us_presidential_speeches. The user is notified about this with the following message:

	The path you entered, (--path), does not lead to a valid directory.
        Returning back to the default directory:

	(default_directory)

3. : Up to five terms can be processed at once. Should more than five terms be inputted, the program will quit instead of executing the general workflow. 

## ----Design-----
No class included.
Using argparse to enable the four arguments 'terms','--path', '--title', and '--output';

First, all the relevant information from the json files is extracted and stored in a data dictionary.

The dictionary has 4 keys: 
1. speeches -  all the speeches are gathered in a list as so that we can fit the vectorizer on the data.
2. dates -  where the value is a list of dates (modifie for better readability).
3. scores - the value is a list of tf-idf scores for each term provided in the input by the user.
4. terms - a list of terms corresponding to the respective dates and scoores. 

Having gathered all the speeches in a list as a value of the key 'speeches', we can then apply the vectorizer on the list, thus calculating the tf-idf scores for each term. Lastly, we can use indexes to retrieve the accurate tf-idf scores, which are then stored in the same dictionary under the key 'scores'.  

Since our dictionary has an equal amount of entries for the values of 'dates', 'scores', and 'terms', the three key-value pairs are transformed into a pandas DataFrame. Lastly, the DataFrame is visualised using seaborn line plot with a few adjustments for better readability. 

* Developed according to the instructions of the Advanced Programming course at Uppsala University.