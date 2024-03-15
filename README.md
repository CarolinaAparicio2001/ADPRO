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

Our repository is structured as follows:

- In the main directory, you can find our showcase notebook ```showcase_notebook.ipynb```. It contains an analysis of the data and showcases our findings.
- `python_files/`: Contains the python code files:\
    - `class_airplane.py`: Python class `Airplane` with several methods was created. All the methods used belong to this class.\
    - `distance_airports.py`: There is a function called `distance_geo` that calculates the geographical distance between two points using latitude and longitude coordinates. It works independently and has robust error handling, returning 0 in case of calculation failures.
- `flight_data/:` Contains our datasets

To use the functionalities provided by the `Airplane` class, follow these steps:

1. Clone this repository to your local machine

2. Run the ```download_data``` method first. It will download the flight data from GitHub and save it to a folder called downloads.

3. Initiate the merging process by running the `merge_datasets` method provided in the `Airplane` class to extract valuable insights, identify patterns, and make data-driven decisions with the downloaded data.


## Airplane Class

The class adheres to PEP8 standards, utilizing black and pylint for code formatting and linting.

```Airplane has several methods:```

1. **download_data:**
   -  Downloads flight data from GitHub, saves it to a download folder and creates Pandas DataFrames for airlines, airplanes, airports, and routes.
   -  Usage: `airplane.download_data()`
2. **merge_datasets:**
   -  Merges the various datasets into a single DataFrame, preparing it for analysis.
   -  Usage: `airplane.merge_datasets()`
3. **plot_airports_in_country:**
   - Plots all airports within a specified country, indicating their locations on a national map.
   - Usage: `airplane.plot_airports_in_country(country)`
4. **distance_analysis:**
   - Calculates the geographical distance between source and destination airports and creates a histogram to visualize the distribution of these distances.
   - Usage: `airplane.distance_analysis()`
5. **plot_flights_by_code_airports:**
   - Visualizes the number of flights originating from a specific airport, providing flexibility to focus on either domestic or all flights.
   - Usage: `airplane_instance.plot_flights_by_code_airports(code_airport, internal=False)`
6. **plot_most_used_airplane_models:**
   - Displays a bar chart of the most frequently used airplane models in the dataset or within a specified set of countries.
   - Usage: `airplane.plot_most_used_airplane_models(countries = None)`
7. **plot_flights_by_country:**
   - This method presents flight distribution from a specified country and allows a focus on domestic flights.It calculates carbon emissions reductions for short-haul flights, providing insights into the environmental impact of air transportation.
   - Usage: `airplane_instance.plot_flights_by_country(country, internal=False, cutoff_distance=500)`
8. **aircrafts:**
   - Lists the aircraft models available in the dataset.
   - Usage:
9. **aircraft_info:**
   - Provides detailed information about a specific aircraft model, including its IATA code and ICAO code.
   - Usage: 
10. **airport_info:**
   - Provides detailed information about a specific airport, including its ID, source airport, city, latitude, and longitude.
   - Usage:

     
## Airplane Class
The class is PEP8 compliant, using black and pylint.


## License
GPL-3.0 license

## Project Status
In Progress