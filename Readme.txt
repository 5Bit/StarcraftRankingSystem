Stacraft 2 Player Recommender System
Developed by Thomas S. Field
Developed during the Spring Quarter, 2017 at DePaul University

External Packages used in this project:
-------------------------------------------------------------------------------
Pandas, Numpy

How to use:
-------------------------------------------------------------------------------

1) verify you have python, Pandas and Numpy installed.

2) Verify you have extracted the program correctly. For reference, the bin
folder must contain "__ini__.py", "FileManager.py", "menuClasses.py",
"Preprocessing.py", "RecommenderSystem.py". The main folder must contain 4
folder: "bin", "data", "output", "toClassify". It must also contain
"preprocessing.ini", "RecommenderSystem.ini", "SC2Rec.py".

3) Add any users you want to classify in the toClassify folder, following the
format of toClassTest.csv. All lines must be filled and not contain NaN data.

4) Add your training data for your Recommender System to the "data" folder.
Added must be in a .csv file. The program will scan the folder for all csv,
verify they meet expectations, and it will handle cleaning and normalization
based on your "AcceptableLoss" setting in preprocessing.ini. For a description
of preprocessing.ini, look at the end of this Readme.

5) To run, open CMD or a Terminal and type the following line while in the
main folder:
>python SC2Rec.py

Simply follow the menu system after which.

Output will not only be printed to the screen, but saved to the output folder.
The output folder will also contain the normalized training data. Output files
will not overwrite one another - instead, each output file is given a unique
timestamp indicating when it ran in the following format:
|YEARMONTHDAYHOURMINUTESECOND|OUTPUT.Filetype
Filetype is dependent on if it is output text or the normalized data. 
Normalized data is stored as .csv files with comma seperations. Output text is
stored as .txt files.

Happy Matchmaking!


Descriptions of functionalities
-------------------------------------------------------------------------------
The following are descriptions on how each subsystem works. 

[RecommenderSystem.py]---------------------------------------------------------
The recommender system, when instanciated, requires a copy of the column Data
(averages and standard deviation for each column) and a copy of the dataframe
after it has been normalized.
When told to classify a user, it is given a user and K (which is specified
in RecommenderSystem.ini). The RS system then normalizes the user according to
the information gathered while normalizing the original data given. With this
"normalized" user, it groups the original table by league, and compares the
new user to each league, finding K similar. It calculates the average 
cosine Similarity, and chooses the largest similarity to be the group the user
is matched with. It finally returns a list containing the league number, the
average for the optimal league, and the top K of the optimal lague.

[menuClasses.py]---------------------------------------------------------------
The menu classes are built on a simple class inheritance system. The parent for
a menu class is menu, which contains the function for prompting the user for a
given number of options.

The MainMenu inherets from the the menu class. The MainMenu class, when
instanciated, constructs itself, prints the disclaimer. When it's run() is
called, it provides the menu to the user - containing options:
-Generate a new Recommender System
-Quit

The RsMenu (Recommender System Menu), when instanciated, reads the preprocessor
configuration .ini file (preprocessing.ini) and stores the data locally. When
the RSmenu instance is told to run(), it then creates a FileManager() instance,
which handles importing all data stored within the data folder. Said data is
provided to the RsMenu. The user is then given three options:
- Request a recommendation for a player
- Data Statistics
- Return to Main Menu

If a user chooses to return to the main menu, it simply returns.

If a user chooses the Data Statistics, the cleaned data is then grouped by
league and provides a description - saved both in output and printed. The
data is the count, mean, std, min, max, and 25%, 50% and 75% quartiles of each
column in the data.

if a user chooses to request a recommendation for a player, the system
automatically calls a preprocessor and provides it the acceptableloss 
percentage. For a description of the preprocessing system, look at the 
PreProcessing class. The preprocessor is told to clean the data and normalize 
it. After which, the RsMenu creates a Recommender System instance (RSI), and 
passes it the relevant data.

[PreProcessing.py]-------------------------------------------------------------
The Preprocessor class is a beast, if I do say so myself. When instanciated, it
expects to be given the acceptableLoss as a number out of 100 (for example, 50
would mean 50% acceptable loss of data). When the preprocessor is told to
CleanData(data), it expects to be given the data to clean. This process prompts
the user it is cleaning the data, and provides a list of rows containing Nans
from the data provided. 
Recording the columns that contain a NaN, the function then goes through each
row and analyzes which rows contain a NaN. It also gets the number of Nan per
each row. By then calculating the min and Maximum number of nans per rows, it
then first checks if there is more rows than 0. If there is, it first checks
if the number of rows with nan is less than the acceptable loss. If it is,
it simply removes the rows with nans, and returns the cleaned data.
If there isn't more rows than acceptable loss, it then first drops all rows
missing league information - after all, if that is missing a row is worthless.
Then the preprocessor checks if it is now under acceptable loss. If it is, the
user is told "The amount of data lost is more than the acceptable losses." and
it suggests adjusting expectations or gathering more data. Otherwise, if the
next amount of data (current rows -1) is under or equal to the acceptable loss,
it returns the data. If that isn't the case, the system then cuts rows with
more Nans, and continues to cut rows with more Nans first until it meets
acceptable loss with the least amount of Nans. If no data is left after this
process, the system tells the user no data is left after cleaning, and it
suggests adjusting expectations or gathering more data. Otherwise, it returns
the data.

When the RsMenu calls Normalization(data), it first drops the GameID. It then
fills any NaNs left after Cleaning with the average of that column/attribute.
it then calculates Z-score for each item, and replaces all values with their
Z-scores. ZScore(data) also stores the columnMean and the columnStddev for
later when comparing new users. This part may be flawed, as it presumes the
next user follows patterns seen in previous users. That said, this also allows
the values for each item to act also as a weight, as it is presumed each
league will follow a pattern within this standard deviation. Finally, the
normalized data is provided to the RSMenu.

[FileManager.py]---------------------------------------------------------------
The FileManager, when instanciated, first acquires the positions for the data
folder, output folder, and toClassify folder. It also generates an output file.

FileManager.getDataFolderContent() acquires the names of files in the data
folder.

FileManager.getAllDataFiles() imports all .csv files held within the data
folder and makes them into pandas dataframes. It assumes all files are
seperated by commas(,).

FileManager.geClassifyFolderContent() acquires the names of files in the 
toClassify folder.

FileManager.getAllClassifyFiles() imports all .csv files held within the 
toClassify folder and makes them into pandas dataframes. It assumes all files
are seperated by commas(,).

__genOutputFolderContent() is a private function for acquring the output 
folder's content and to avoid overwritting any previous output files.

__genTimestamp() is a private function to generate a timestamp for generated
files. 

__genOutputFileName(filetype) is a private function that generates an output
filename if given the filetype.

saveDF(df) is a function that saves the designated dataframe as a new file.

updateOutputTextFile(newText) Updats the output.txt file for the current
process. The text given is added to the file for this process.

[Statistics.py]----------------------------------------------------------------
Rather simple in comparison to the rest of the system, Statistics.py just
contains one class - the Statistics class. This one simply groups the data it
is given in construction. 

When getStatistics() is called, it widens numpy's print column info, and prints
the statistics per each league. It also provides the data to the MainMenu so it
can store it in the output file.


Instructions for modifying preprocessing.ini
-------------------------------------------------------------------------------

[SectionOne]-------------------------------------------------------------------
This section is for CLEANING settings. These settings will be utilized by the
system to determine how much data to keep.
 
 
acceptableLoss  : Is the acceptable percentage of the data lost. (default is
50%, but this assumes a large dataset. acceptableMin has priority over this.)



Instructions for modifying RecommenderSystem.ini
-------------------------------------------------------------------------------

[SectionOne]-------------------------------------------------------------------
This section is for Recommender System settings. These settings will be
utilized by the system to determine functionality of the Recommender System.
 
 
k  : K is used for calculating the distance to each league. For each league,
the Recommender System finds the K most similar players and calculates the
Cosine Similarity to those players. It then calculates the average distance of
the K, using that as the ranking calculation.