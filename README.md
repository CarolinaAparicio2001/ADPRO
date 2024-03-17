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

- In the main directory, you can find:
    -  our showcase notebook ```showcase_notebook.ipynb```. It contains an analysis of the data and showcases our findings.
    -  ```environment.yml```. The YAML file contains a list of all the essential dependencies required to run our project.
    -  ```gitignore```. This file contains patterns for Git to ignore, specifically for Python projects. It excludes files like byte-compiled code, log files, and local configurations to maintain a clean repository.
- `docs/`: Contains the documentation files generated with Sphinx:
  - `class_airplane.rst`: Provides a detailed explanation of the `Airplane` class, outlining the methods for downloading and analyzing airplane data, including retrieving information on specific aircraft and airports.
  - `conf.py`: This file contains key configurations essential for customizing Sphinx documentation's appearance and structure.
  - `distance_airports.rst`: This document explains the distance_airports module, including its function to compute the geodesic distance between airports and its usage scenarios.
  - `distance_function_test.rst`: Describes tests for verifying distance calculations in the `TestDistanceGeo` class, ensuring function accuracy and reliability.
  - `index.rst`: The navigation page guides users to specific sections in the document.
  - `make.bat`and `Makefile`: These scripts assist in generating documentation using Sphinx, accommodating various build options and environments.
  - `modules.rst`: Compiled by Sphinx, this file lists all documented modules in the project, serving as a quick reference.
- `flight_data/:` Contains our datasets
- `python_files/`: Contains the python code files:
    - `class_airplane.py`: Python class `Airplane` with several methods was created. All the methods used belong to this class.
    - `distance_airports.py`: There is a function called `distance_geo` that calculates the geographical distance between two points using latitude and longitude coordinates. It works independently and has robust error handling, returning 0 in case of calculation failures.
    - `distance_function_test.py` : Python class `TestDistanceGeo` where is included the 3 unit tests for the function `distance_geo`from `distance_airports.py`.


To use the functionalities provided by the `Airplane` class, follow these steps:

1. Clone this repository to your local machine

2. Run the ```download_data``` method first. It will download the flight data from GitHub and save it to a folder called downloads.

3. Initiate the merging process by running the `merge_datasets` method provided in the `Airplane` class to extract valuable insights, identify patterns, and make data-driven decisions with the downloaded data.

4. For the LLM, to have access to OPENAI_API_KEY we had to use "import os" and we deleted before uploading to git. Maybe there is need to some adjustments before these codes starts working.

5. Run the following command to create a new environment named `airplane_05` using the provided `environment.yml`:
   ```shell
   conda env create -f environment.yml
   ```
6. List all available Conda environments to confirm that environment has been created successfully:
   ```shell
   conda info --envs
   ```
7. Once confirmed, activate the new environment with:
   ```shell
   conda activate airplane_05
   ```
9. To generate and view the project´s documentation ensure you have Sphinx installed. If not already installed, run the following on your environment:
   ```shell
   conda install sphinx sphinx_rtd_theme make
   ```
10. To access the documentation, go to the `docs` folder and execute the command.
   ```shell
    mkdir docs
    cd docs
   ```
    
To use the functionalities provided by the `TestDistanceGeo` class, follow these steps:

1. Ensure that both `distance_airports.py` and `distance_function_test.py` files are located within the `python_files/`. These files contain the implementation of the distance calculation and the corresponding unit tests, respectively.

2. Make sure you installed geopy before starting to test. In not already installed, use pip: 
   ```bash
   pip install geopy 
   ```
3. Open a terminal Jupyter Lab. Ensure you navigate to the directory containing the two Python files mentioned above. If you are not already in the correct directory, you can change directories using the cd command.
4. In the terminal, code:
   ```bash 
   python distance_function_test.py
   ```
This command will run the 3 tests defined in the TestDistanceGeo class. If everything is set up correctly, you should see output indicating the execution time and a status of "OK" meaning that all tests passed successfully.


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
   - Usage: `airplane.plot_flights_by_code_airports(code_airport, internal=False)`
6. **plot_most_used_airplane_models:**
   - Displays a bar chart of the most frequently used airplane models in the dataset or within a specified set of countries.
   - Usage: `airplane.plot_most_used_airplane_models(countries = None)`
7. **plot_flights_by_country:**
   - This method presents flight distribution from a specified country and allows a focus on domestic flights.It calculates carbon emissions reductions for short-haul flights, providing insights into the environmental impact of air transportation.
   - Usage: `airplane.plot_flights_by_country(country, internal=False, cutoff_distance=500)`
8. **aircrafts:**
   - Lists the aircraft models available in the dataset.
   - Usage: `airplane.aircrafts()`
9. **aircraft_info:**
   - Provides detailed information about a specific aircraft model, including its IATA code and ICAO code.
   - Usage: `airplane.aircraft_info(aircraft_name)`
10. **airport_info:**
   - Provides detailed information about a specific airport, including its ID, source airport, city, latitude, and longitude.
   - Usage: `airplane.airport_info(airport_name)`


## TestDistanceGeo Class

The class adheres to PEP8 standards, utilizing black and pylint for code formatting and linting.

1. **test_distance_geo_same_location:** 
   - Tests distance with same airport as source and destination airport.

2. **test_distance_geo_different_airports_same_country:** 
   - Test distance from different airports at the same country.

3. **test_distance_geo_different_countries:** 
   - Test distance from airports from different countries.


## Airplane Class
The class is PEP8 compliant, using black and pylint.


## TestDistanceGeo Class
The class is PEP8 compliant, using black and pylint.


## License
GPL-3.0 license


## Project Status
Finished