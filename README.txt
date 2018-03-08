Luis Solorzano 
Implement the ID3 algorithm for learning decision trees (with human-interpretable
learning), and evaluate and compare the performance of two machine learning algorithms on empirical
data sets (monk1.csv and opticalDigit.csv).

###############################################################
OBJECTIVE: 
Assign correctly predict an instance based off of training sets.


###############################################################
DATA SETS:
1. monks1.csv: A data set describing two classes of robots using all nominal attributes and
a binary label. This data set has a simple rule set for determining the label: if
head_shape = body_shape OR jacket_color = red, then yes, else no.
Each of the attributes in the monks1 data set are nominal. Monks1 was one of the first
machine learning challenge problems (http://www.mli.gmu.edu/papers/91-95/91-28.pdf).
This data set comes from the UCI Machine Learning Repository:
http://archive.ics.uci.edu/ml/datasets/MONK%27s+Problems


2. opticalDigit.csv: A data set of optical character recognition of numeric digits from
processed pixel data. Each instance represents a different 32x32 pixel image of a
handwritten numeric digit (from 0 through 9). Each
image was preprocessed into a smaller number of attributes. Each image was partitioned
into 64 4x4 pixel segments and the number of pixels with non-background color were
counted in each segment. These 64 counts (ranging from 0-16) are the 64 attributes in
the data set, and the label is the number from 0-9 that is represented by the image. This
data set is more complex than the Monks1 data set, but still contains only nominal
attributes and a nominal label. This data set comes from the UCI Machine Learning
Repository:
http://archive.ics.uci.edu/ml/datasets/Optical+Recognition+of+Handwritten+Digits


3. tennis.csv: A dataset used for testing. This short dataset has four variables: outlook, temperature, humidity, and windy.
It also has only two labels which are "yes" if it is a good day to play tennis, or "no" it is not a good
day to play tennis. 



###############################################################
PARAMETERS:
There are three parameters that must be passed when calling ID3. 
1. First the path to a file containing a data set(e.g., monks1.csv)

2. The percentage of instances to use for a training set. Please use decimals
for example in order to use 75% of data for training type in 0.75

3. A random seed as an integer. (e.g., 12345)

example call in terminal: python3 id3 monks1.csv 0.75 12345

###############################################################
OUTPUT:
Printing a confusion matrix for our predictions on testSet
this is the outputted to the current directory as a csv file
if user makes "python3 ID3.py monks1.csv 0.75 12345", then the
output file will be titled 'results_ID3_monk1.csv_12345.csv'


###############################################################