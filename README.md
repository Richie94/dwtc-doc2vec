# dwtc-doc2vec
Welcome to dwtc-doc2vec
You can find here the source code for my project.

As a short overview:
- look at src/config.py to set/create folders correctly
- for preprocessing data you need to load the unpacked mannheim web corpus data in the specified folder in config, then you can run it and it will output the processed files into the keep folder
- for caltulating models write the wanted models into targetCombinations.txt and start main.py, alternatively comment this line in main file out and use the getParameterCombinations which is commented out
