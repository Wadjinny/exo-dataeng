
## Overview
In this exercice, we have to merge two Excel files (A and B), A being a raw Table that contains possible typos and B being a reference table. The goal is to merge the two tables.  

__To do so, we will follow this steps:__
1. Data Cleaning
2. Matching
3. Merging

## Data Cleaning

First step is to clean the imported excel files. Knowing that the actual tables could be anywhere in the excel file, we will first trime the tables and then clean them. This process will consist of:

1. Droping empty columns and rows
2. Setting the first row as column headers

Second step is to clean text data in both datasets. We will:

1. Strip leading and trailing whitespace
2. Remove extra spaces within text
3. Convert text to lowercase

This will help standardize the text data for accurate matching later in the process.

## 2. Matching 

In order to match between the mispeled names in Table A and names in Table B, we have to work with full names, and by concatinating first and last names from Table B, we can apply a matching strategy to find the matching full names:

1. Combines first and last names in DataFrame B
2. Applies a matching strategy to find matching full names in the same city (fuzzy matching, exact matching)


Fuzzy matching works by comparing the similarity between two strings and returning a score that indicates how closely they match. To correct the typos, we will choose a 87% similarity threshold. This treshold is chosen based on experimentation and can be adjusted if needed. 

## 3. Merging

After correcting the typos in Table A, we can merge the two datasets based on the matched full names and city.



