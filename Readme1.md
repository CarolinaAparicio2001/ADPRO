# Project Agros: analysis of the world’s agricultural output

## Description
The repository contains our advanced programming group project, using data on agriculture by Our World in Data, analyzing the world’s agricultural production between the years 1961 and 2019. The goal is to contribute to the green transition.

The project is part of the Advanced Programming Course at Nova SBE. Our main analysis can be found in the showcase Jupyter Notebook. Here, the agricultural evolution of several countries is analyzed with a comparison of the outputs, a gapminder plot, a correlation matrix, area graphs, a choropleth map, and finalized with a prediction of the countries' outputs. 

The project is shared work by Group 11:\
Julia Stieler - 56040, 56040@novasbe.pt\
Hannah Dickescheid - 50178, 50178@novasbe.pt\
Carlos Ferrufino - 53276, 53276@novasbe.pt\
Eva Zinser - 53100, 53100@novasbe.pt


## Data
We are using data on Agricultural total factor productivity (USDA), downloaded from Our World in Data, (datasource can be found [here](https://github.com/owid/owid-datasets/tree/master/datasets/Agricultural%20total%20factor%20productivity%20(USDA)))

The original data was published by the United States Department for Agriculture (USDA) Economic Research Service.


## Getting started
1. Our repository is structured as follows: In the main directory, you can find our showcase notebook ```showcase_notebook.ipynb```. It contains an analysis of the data and showcases our findings. For the project, a class named ```Airplane``` with several methods was created. All the methods used belong to this class. The file ```class_airplane.py``` containing the class can be found in the python_files directory.

2. Run the ```download_data``` method first. It will download the flight data from GitHub and save it to a folder called downloads.


## Agros Class
The class adheres to PEP8 standards, utilizing black and pylint for code formatting and linting.

```Airplane has several methods:```

1. download_data: Downloads flight data from GitHub, saves it to a download folder, and creates Pandas DataFrames for airlines, airplanes, airports, and routes.
2. merge_datasets: Merges the various datasets into a single DataFrame, preparing it for analysis.
3. distance_analysis: Calculates the geographical distance between source and destination airports and creates a histogram to visualize the distribution of these distances.
4. plot_airports_in_country: Plots all the airports in a selected country, marking them on a map.
5. plot_flights_by_code_airports: Visualizes the number of flights originating from a specific airport, showing the most common destinations.
6. plot_most_used_airplane_models: Displays a bar chart of the most frequently used airplane models in the dataset or within a specified set of countries.
7. plot_flights_by_country: Shows the number of flights departing from a particular country, with the option to focus on internal (domestic) flights.
8. plot_airports_in_country: Plots all airports within a specified country, indicating their locations on a national map.

## License
GPL-3.0 license

## Project Status
End Sprint :)

## Special Thanks 
to Luis and Our World In Data
