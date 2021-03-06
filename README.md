# Fantasy Football Data Analysis
A Python program to scrape data from the web which is cleaned to perform data analysis. This simple project is an introduction into the Python machine learning library scikit-learn as well as an introduction to R for data visualization.

Project was based off of the 'fftiers' program found on Github.


## Python
Historical fantasy data pulled from: www.pro-football-reference.com which is parsed and written to local directory as csv files.

Historical rankings data output:
- Specific season years
- Collection of recent past five seasons
- Past five seasons split by player position
- ...


Expert consensus rankings data is used for generating player tier projections.
Data is pulled from: www.fantasypros.com

Parsed expert consensus data formats:
- Overall (QB, RB, WR, TE, K, DST)
- By specific position


Collected data is run through a k-means clustering algorithm that generates ranking tiers.
The scikit-learn library was used for the k-means clustering implementation.

Clustered tier rankings data is then written to local directory as csv files.


## R
Using csv files generated by python process, clustered rankings data is plotted using ggplot2.
- x-axis: Expert Average Rank
- y-axis: Expert Consensus Rank
- color-coded according to tiers
