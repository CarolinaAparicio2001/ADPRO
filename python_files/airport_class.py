""" This module contains one class with the purpose of analyzing agricultural data internationally.
It contains seven methods. Those can download the data, list all the countries of the dataset,
provide a correlation matrix of the outputs, and plot an area chart of the agricultural output
of a choosen country.
It can also compare the output of choosen countries with a line graph, and plot a scatter plot
of fertilizer and output quantity.
Moreover, a choropleth of the total factor productivity for a selected year can be plotted.
Lastly, an ARIMA prediction for the total factor productivity is applied and the data
including the prediction is plotted.
"""

import warnings
import os
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from pmdarima.arima import auto_arima

warnings.filterwarnings("ignore")


class Agros:
    """
    A class that downloads agricultural data and performs analysis on it.

    Attributes
    ---------------
    data_df: Pandas Dataframe
        dataframe where the downloaded agricultural data can be loaded into

    merge_dict: dict
        a dictionary in order to change the spelling for some countries to allow merging

    geopandas_df: Geopandas df
        a geopandas dataframe where geo dataset with country-level polygons can be loaded into


    Methods
    ---------------
    download_data
        downloads agricultural data from Github, saves it to a download folder
        and creates Pandas DataFrame

    list_countries
        list all the available countries of the dataset

    correlate_quantity
        provides a correlation heatmap of the quality columns

    area_graph
        provides an area graph of the outputs of a selected country or the world

    compare_output
        plots the output columns of selected countries

    gapminder
        provides a scatterplot of fertilizer and output quantity for a selected year

    choropleth
        provides a choropleth plotting the total factor productivity of a selected year

    predictor
        applies an ARIMA prediction for the total factor productivity and
        plots the data including the prediction
    """

    def __init__(self):
        self.data_df = pd.DataFrame
        self.merge_dict = {
            "United States of America": "United States",
            "Dem. Rep. Congo": "Democratic Republic of Congo",
            "Dominican Rep.": "Dominican Republic",
            "Timor-Leste": "Timor",
            "Eq. Guinea": "Equatorial Guinea",
            "eSwatini": "Eswatini",
            "Solomon Is.": "Solomon Islands",
            "N. Cyprus": "Cyprus",
            "Somaliland": "Somalia",
            "Bosnia and Herz.": "Bosnia and Herzegovina",
            "S. Sudan": "South Sudan",
        }
        self.geopandas_df = gpd.GeoDataFrame

    def download_data(self):
        """
        Creates a 'downloads' folder, if it doesn't exist.
        Downloads agricultural data from Github repository and saves it to this folder,
        in case it is not already downloaded.
        It also creates Pandas Dataframe from the downloaded csv file.
        It also cleans the data so that aggregated rows (like Asia) are excluded.
        """
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        exists = os.path.isfile("downloads/download.csv")

        if not exists:
            response = requests.get(
                "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/"
                "Agricultural%20total%20factor%20productivity%20(USDA)"
                "/Agricultural%20total%20factor%20productivity%20(USDA).csv"
            )
            with open("downloads/download.csv", "wb") as file:
                file.write(response.content)

        data_df = pd.read_csv("downloads/download.csv")
        countries_to_drop = [
            "Asia",
            "Caribbean",
            "Central Africa",
            "Central America",
            "Central Asia",
            "Central Europe",
            "Developed Asia",
            "Developed countries",
            "East Africa",
            "Eastern Europe",
            "Former Soviet Union",
            "High income",
            "Horn of Africa",
            "Latin America and the Caribbean",
            "Least developed countries",
            "Lower-middle income",
            "North Africa",
            "North America",
            "Northeast Asia",
            "Northern Europe",
            "Oceania",
            "Pacific",
            "Sahel",
            "South Asia",
            "Southeast Asia",
            "Southern Africa",
            "Southern Europe",
            "Sub-Saharan Africa",
            "Upper-middle income",
            "West Africa",
            "West Asia",
            "Western Europe",
            "World",
            "Low income",
        ]
        data_df = data_df.loc[~data_df["Entity"].isin(countries_to_drop)]
        self.data_df = data_df

        self.geopandas_df = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
