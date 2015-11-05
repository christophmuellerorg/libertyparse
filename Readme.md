libertyparse 
================
This is a very simple parser for liberty library files returning a dictionary structure resembling the structure of the file. Parsing is done using pyparsing and can be slow for large library files. However, since the library files are not likely to change too frequently it is possible to pickle the data structure for faster access later. 

The code is in a working state for the library files I used it with, however there is no warenty for the grammar being complete. If you run into trouble please let me know, I will accept pull request happily.
