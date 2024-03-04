""" This module contains one class with the purpose of analyzing the internal flight.
"""

import os
import requests
import pandas as pd
from io import BytesIO
from zipfile import ZipFile

class Airplane:
    """
    A class to download airplane data and perform analysis on it.
    """

    def __init__(self):
        self.airlines_df = pd.DataFrame()
        self.airplanes_df = pd.DataFrame()
        self.airports_df = pd.DataFrame()
        self.routes_df = pd.DataFrame()

    def download_data(self):
        """
        Checks for a 'downloads' folder and creates it if it doesn't exist.
        Downloads flight data from a GitHub repository as a zip file, saves it,
        extracts the contents, and creates Pandas DataFrames from the CSV files:
        - airlines.csv
        - airplanes.csv
        - airports.csv
        - routes.csv
        """
        
        downloads_dir = "downloads"
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)

        zip_file_path = os.path.join(downloads_dir, "flight_data.zip")

        '''Check if the zip file was already downloaded'''
        if not os.path.exists(zip_file_path):
            response = requests.get(
                "https://gitlab.com/adpro1/adpro2024/-/"
                "raw/main/Files/flight_data.zip?inline=false",
                stream=True
            )
            '''Ensure the request is successful'''
            if response.status_code == 200:
                with open(zip_file_path, "wb") as f:
                    f.write(response.content)

        '''Extract files if the zip file is downloaded'''
        if os.path.exists(zip_file_path):
            with ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(downloads_dir)

                '''Loading data into DataFrames'''
                self.airlines_df = pd.read_csv(os.path.join(downloads_dir, 'airlines.csv'))
                self.airplanes_df = pd.read_csv(os.path.join(downloads_dir, 'airplanes.csv'))
                self.airports_df = pd.read_csv(os.path.join(downloads_dir, 'airports.csv'))
                self.routes_df = pd.read_csv(os.path.join(downloads_dir, 'routes.csv'))

        '''Print the first 5 lines of each dataset'''
        print("Airlines DataFrame:\n", self.airlines_df.head())
        print("\nAirplanes DataFrame:\n", self.airplanes_df.head())
        print("\nAirports DataFrame:\n", self.airports_df.head())
        print("\nRoutes DataFrame:\n", self.routes_df.head())

        print("\nDownloaded data executed!")

