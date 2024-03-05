# Group_05 Project Icaras: analysis of commercial airflight data for a sustainability study

## Description

This repository contains our advanced programming group project, which focuses on analyzing flight data from the International Air Transport Association. The objective of this project is to explore and understand trends, efficiency, and dynamics within the global aviation industry. Our analysis aims to contribute to enhancing flight efficiency and reducing environmental impacts, aligning with the broader goal of the green transition.

The project is part of the Advanced Programming course at Nova SBE. The project's primary objective is to enhance flight planning by analyzing aviation data. Our Jupyter Notebook focuses on investigating flight routes, airport connectivity, and flight distances to promote sustainable aviation practices. By examining flight networks and analyzing distance frequencies, we hope to uncover insights that can lead to more efficient and environmentally friendly flight planning. This project combines advanced programming skills with real-world challenges to contribute to the future of sustainable aviation.

The project is shared work by Group 5:\
Carolina Aparicio - 61582, 61582@novasbe.pt\
Erica Francalanci - 61600, 61600@novasbe.pt\
Julia Cheng - 60490, 60490@novasbe.pt\
Sara Favita - 60141, 60141@novasbe.pt

## Data
We will be using data from [International Air Transport Association](https://www.iata.org/). The datasets can be found [here](https://gitlab.com/adpro1/adpro2024/-/raw/main/Files/flight_data.zip?inline=false).


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

## Airplane Class
The class is PEP8 compliant, using black and pylint.


## License
GPL-3.0 license

## Project Status
In Progress