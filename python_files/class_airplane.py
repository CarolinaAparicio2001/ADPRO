"""
Module: class_airplane

Description: This module defines the Airplane class for downloading airplane data and performing analysis on it.
"""

# Standard libraries
import os
from zipfile import ZipFile
import random
from difflib import get_close_matches
import requests


# Third-party libraries
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
from plotnine import ggplot, aes, geom_histogram, theme_minimal, scale_fill_manual
from langchain_openai import ChatOpenAI

# Local application libraries
from distance_airports import distance_geo


class Airplane:
    """
    A class to handle the downloading, merging, analysis, and visualization of airplane data.

    Attributes:
    -----------
    airlines_df (DataFrame): Contains airline data.
    airplanes_df (DataFrame): Contains airplanes data.
    airports_df (DataFrame): Contains airports data.
    routes_df (DataFrame): Contains routes data.
    merge_df (DataFrame): Contains merged dataset for analysis.

    Methods:
    --------
    download_data():
        Downloads flight data from a specified URL and extracts it into the 'downloads' directory.

    merge_datasets():
        Merges airlines, airplanes, airports, and routes datasets into a single DataFrame.

    plot_airports_in_country(country):
        Plots the locations of airports within the specified country.

    distance_analysis():
        Calculates and plots the distribution of distances between source and destination airports.

    plot_flights_by_code_airports(code_airport, internal=False):
        Visualizes flight routes originating from a specific airport. Filters for domestic flights if 'internal' is True.

    plot_most_used_airplane_models(n=5, countries=None):
        Plots the top 'n' most frequently used airplane models based on the number of routes.

    plot_flights_by_country(country, internal=False, cutoff_distance=500):
        Plots flight routes for the specified country, differentiating between short-haul and long-haul flights based on 'cutoff_distance'.

    aircrafts():
        Lists aircraft models present in the dataset.

    aircraft_info(aircraft_name):
        Retrieves and prints detailed information for a specified aircraft model.

    airport_info(airport_name):
        Retrieves and prints detailed information for a specified airport.
    """

    def __init__(self):
        """
        Initializes the Airplane class with empty DataFrames for storing dataset information.
        """
        self.airlines_df = pd.DataFrame()
        self.airplanes_df = pd.DataFrame()
        self.airports_df = pd.DataFrame()
        self.routes_df = pd.DataFrame()
        self.merge_df = pd.DataFrame()

    def download_data(self):
        """
        Download the flight data and save it to a folder called downloads.
        """

        downloads_dir = "downloads"
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        zip_file_path = os.path.join(downloads_dir, "flight_data.zip")
        if not os.path.exists(zip_file_path):
            response = requests.get(
                "https://gitlab.com/adpro1/adpro2024/-/"
                "raw/main/Files/flight_data.zip?inline=false",
                stream=True,
                timeout=10,
            )
            if response.status_code == 200:
                with open(zip_file_path, "wb") as file:
                    file.write(response.content)
        if os.path.exists(zip_file_path):
            with ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(downloads_dir)
                self.airlines_df = pd.read_csv(
                    os.path.join(downloads_dir, "airlines.csv")
                )
                self.airplanes_df = pd.read_csv(
                    os.path.join(downloads_dir, "airplanes.csv")
                )
                self.airports_df = pd.read_csv(
                    os.path.join(downloads_dir, "airports.csv")
                )
                self.routes_df = pd.read_csv(os.path.join(downloads_dir, "routes.csv"))

                """
                Loading data into DataFrames
                """
                self.airlines_df = pd.read_csv(
                    os.path.join(downloads_dir, "airlines.csv")
                )
                self.airplanes_df = pd.read_csv(
                    os.path.join(downloads_dir, "airplanes.csv")
                )
                self.airports_df = pd.read_csv(
                    os.path.join(downloads_dir, "airports.csv")
                )
                self.routes_df = pd.read_csv(os.path.join(downloads_dir, "routes.csv"))

    def merge_datasets(self):
        """
        Merges different datasets and cleans up unnecessary columns.
        """

        self.airlines_df = self.airlines_df.drop(
            self.airlines_df.columns[0], axis=1
        ).reset_index(drop=True)
        self.airports_df = self.airports_df.drop(
            self.airports_df.columns[0], axis=1
        ).reset_index(drop=True)
        self.airports_df = self.airports_df.drop(["Type", "Source"], axis=1)
        self.routes_df = self.routes_df.drop(
            self.routes_df.columns[0], axis=1
        ).reset_index(drop=True)
        self.airplanes_df = self.airplanes_df.drop(
            self.airplanes_df.columns[0], axis=1
        ).reset_index(drop=True)

        merge_df_1 = pd.merge(
            self.airports_df,
            self.routes_df,
            left_on="IATA",
            right_on="Source airport",
            how="left",
        )
        merge_df_1 = merge_df_1.rename(
            columns={
                "Country": "Source country",
                "Latitude": "latitude_source",
                "Longitude": "longitude_source",
            }
        )

        merge_df = pd.merge(
            merge_df_1,
            self.airports_df[["IATA", "Country", "Latitude", "Longitude"]],
            left_on="Destination airport",
            right_on="IATA",
            how="left",
        )
        merge_df = merge_df.rename(
            columns={
                "IATA_x": "IATA",
                "Country": "Destination country",
                "Latitude": "latitude_destination",
                "Longitude": "longitude_destination",
            }
        )
        merge_df = merge_df.dropna(subset=["Source country", "Destination country"])

        merge_df.drop(
            columns=[
                "IATA_y",
                "DST",
                "Tz database time zone",
                "Airline",
                "Timezone",
                "Codeshare",
                "Altitude",
            ],
            inplace=True,
        )

        self.merge_df = merge_df

        return self.merge_df

    def plot_airports_in_country(self, country):
        """
        Plot the locations of airports within a specified country on a map.

        Parameters:
        ---------------
            country (str): The name of the country for which airports are to be plotted.

        Returns:
        ---------------
            None: This method implicitly displays a map plot or prints a message and does
            not have a return statement.
        """

        country_airports = self.merge_df[self.merge_df["Source country"] == country]
        if country_airports.empty:
            print(f"No airports found in {country}.")
            return
        world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        country_map = world[world["name"] == country]
        if country_map.empty:
            print(f"Country '{country}' not found.")
            return
        gdf_airports = gpd.GeoDataFrame(
            country_airports,
            geometry=gpd.points_from_xy(
                country_airports.longitude_source, country_airports.latitude_source
            ),
        )
        fig, ax = plt.subplots(figsize=(10, 10))
        country_map.plot(ax=ax, color="lightgrey")
        gdf_airports.plot(
            ax=ax, marker="o", color="red", markersize=5, label="Airports"
        )

        for idx, row in gdf_airports.iterrows():
            ax.text(row.geometry.x, row.geometry.y, row["Source airport"], fontsize=8)
        plt.title(f"Airports in {country}")
        plt.legend()
        plt.show()

    def distance_analysis(self):
        """
        Performs distance analysis between source and destination airports.

        Parameters
        ---------------
            None: This method does not take any parameters.

        Returns:
        ---------------
            distance_plot (ggplot object): Represents a histogram of distances.
        """

        self.merge_df["distance"] = self.merge_df.apply(
            lambda row: distance_geo(
                row["latitude_source"],
                row["longitude_source"],
                row["latitude_destination"],
                row["longitude_destination"],
            ),
            axis=1,
        )
        distance_plot = (
            ggplot(self.merge_df, aes(x="distance"))
            + geom_histogram(bins=30, fill="#5496BF", color="black")
            + theme_minimal()
            + scale_fill_manual(
                values=["#011526", "#C9DFF2", "#5496BF", "#75B2BF", "#025159"]
            )
        )
        return distance_plot

    def plot_flights_by_code_airports(self, code_airport, internal=False):
        """
        Plots flight routes originating from a specified airport.
        If the 'internal' parameter is set to True, it will display only domestic
        flights within the specified airport's country.
        Otherwise, it displays all flights from the airport on a global map.

        Parameters:
        ---------------
            code_airport (str): IATA code of the source airport.
            internal (bool): Flag for plotting only domestic flights; defaults to False.

        Returns:
        ---------------
            None: This method does not return a value. It displays the plot showing
            flight routes.
        """

        country_of_source = self.merge_df.loc[
            self.merge_df["Source airport"] == code_airport, "Source country"
        ].iloc[0]

        world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        country_geom = world[world["name"] == country_of_source].geometry.unary_union

        if internal:
            flights = self.merge_df[
                (self.merge_df["Source airport"] == code_airport)
                & (self.merge_df["Destination country"] == country_of_source)
                & (self.merge_df["Source country"] == country_of_source)
            ]
        else:
            flights = self.merge_df[(self.merge_df["Source airport"] == code_airport)]

        if flights.empty:
            print(f"No flights found for the specified criteria from {code_airport}.")
            return

        source_points = gpd.points_from_xy(
            flights.longitude_source, flights.latitude_source
        )
        destination_points = gpd.points_from_xy(
            flights.longitude_destination, flights.latitude_destination
        )

        gdf_flights = gpd.GeoDataFrame(flights, geometry=source_points)
        gdf_destinations = gpd.GeoDataFrame(flights, geometry=destination_points)

        fig, axis = plt.subplots(figsize=(10, 10))
        if internal:
            country_plot = world[world["name"] == country_of_source]
            country_plot.plot(ax=axis, color="lightgrey")

            minx, miny, maxx, maxy = country_geom.bounds
            axis.set_xlim(minx, maxx)
            axis.set_ylim(miny, maxy)
        else:
            world.plot(ax=axis, color="lightgrey")
            world[world["name"] == country_of_source].plot(ax=axis, color="lightblue")

        gdf_flights.plot(
            ax=axis, marker="o", color="blue", markersize=20, label="Source Airports"
        )
        gdf_destinations.plot(
            ax=axis,
            marker="^",
            color="green",
            markersize=20,
            label="Destination Airports",
        )

        for src_point, dest_point in zip(source_points, destination_points):
            axis.plot(
                [src_point.x, dest_point.x],
                [src_point.y, dest_point.y],
                color="red",
                linewidth=1,
                marker="",
            )

        plt.title(f"{'Internal' if internal else ''} Flights from {code_airport}")
        plt.legend()
        plt.show()

    def plot_most_used_airplane_models(self, n: int = 5, countries=None):
        """
        Plots the most used airplane models based on the number of routes.

        Parameters:
        ---------------
            n (int): Number of airplane models to plot, defaults to 5.
            countries (list/str): Specific country or list of countries to consider; defaults to None.

        Returns:
        ---------------
            None. This method does not return any value. It displays the plot directly.
        """

        if countries:
            if isinstance(countries, str):
                countries = [countries]
            filtered_routes = self.merge_df[
                self.merge_df["Source country"].isin(countries)
            ]
            top_airplanes = filtered_routes["Equipment"].value_counts().nlargest(n)
        else:
            top_airplanes = self.merge_df["Equipment"].value_counts().nlargest(n)

        top_airplanes.plot(
            kind="bar", title=f"Top {n} Airplane Models by Number of Routes"
        )
        plt.xlabel("Airplane Model")
        plt.ylabel("Number of Routes")
        plt.show()

    def plot_flights_by_country(self, country, internal=False, cutoff_distance=500):
        """
        Plot the map flight routes between domestic and international flights
        from source to destination airports.

        Parameters:
        ---------------
            country (str): Name of the source country.
            internal (bool): If the flight is internal or not.
            Being by default False.
            cutoff_distance (float): Threshold in km to differentiate
            between short-haul and long-haul flights.

        Returns:
        ---------------
            None. This method does not return any value but displays directly the plot.
        """

        if "distance" not in self.merge_df.columns:
            self.distance_analysis()

        if internal:
            internal_routes = self.merge_df[
                (self.merge_df["Source country"] == country)
                & (self.merge_df["Destination country"] == country)
            ]

            if internal_routes.empty:
                print(f"No routes found for {country}.")
                return

            world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
            country_map = world[world["name"] == country]
            if country_map.empty:
                print(f"Country '{country}' not found.")
                return

            _, axis = plt.subplots(figsize=(10, 10))
            country_map.plot(ax=axis, color="lightgrey")

            total_short_haul_distance = 0
            no_double_routes = set()
            short_haul_count = 0

            for _, row in internal_routes.iterrows():
                round_trip_airports = tuple(
                    sorted([row["Source airport"], row["Destination airport"]])
                )
                if round_trip_airports not in no_double_routes:
                    distance = row["distance"]
                    if distance <= cutoff_distance:
                        total_short_haul_distance += distance
                        short_haul_count += 1
                        no_double_routes.add(round_trip_airports)
                        color = "tomato"
                    else:
                        color = "midnightblue"

                    route = LineString(
                        [
                            Point(row["longitude_source"], row["latitude_source"]),
                            Point(
                                row["longitude_destination"],
                                row["latitude_destination"],
                            ),
                        ]
                    )
                    gpd.GeoDataFrame(geometry=[route]).plot(
                        ax=axis, color=color, linewidth=2
                    )

            plt.annotate(
                f"Total short-haul flights: {short_haul_count}\nTotal short-haul distance: {total_short_haul_distance:.2f} km",
                xy=(0.07, 1.2),
                xycoords="axes fraction",
                fontsize=12,
                backgroundcolor="white",
            )

            plt.legend()
            plt.title(
                f"Internal flights within {country} (Cutoff: {cutoff_distance}km)"
            )
            plt.show()

        else:
            all_routes = self.merge_df[(self.merge_df["Source country"] == country)]
            if all_routes.empty:
                print(f"No routes found for {country}.")
                return

            world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
            _, axis = plt.subplots(figsize=(10, 10))
            world.plot(ax=axis, color="lightgrey")

            total_short_haul_distance = 0
            no_double_routes = set()
            short_haul_count = 0

            for _, row in all_routes.iterrows():
                round_trip_airports = tuple(
                    sorted([row["Source airport"], row["Destination airport"]])
                )
                if round_trip_airports not in no_double_routes:
                    distance = row["distance"]
                    if distance <= cutoff_distance:
                        total_short_haul_distance += distance
                        short_haul_count += 1
                        no_double_routes.add(round_trip_airports)
                        color = "tomato"
                    else:
                        color = "midnightblue"

                    route = LineString(
                        [
                            Point(row["longitude_source"], row["latitude_source"]),
                            Point(
                                row["longitude_destination"],
                                row["latitude_destination"],
                            ),
                        ]
                    )
                    gpd.GeoDataFrame(geometry=[route]).plot(
                        ax=axis, color=color, linewidth=2
                    )

            """
            This section compares the potential carbon emission reductions 
            between short-haul flights and equivalent train rides.
            Supposing that a domestic flight emits 246 grams per kilometer, 
            calculate the total kilometer of short-haul flights times 246
            Next, we consider the environmental impact of short-haul flights 
            compared to train rides.
            Research indicates that short-haul flights covering a 
            distance of less than 500 km can produce three times more CO2 emissions 
            than a train ride over the same distance.
            Hence, to estimate the emissions from equivalent train rides, 
            we divide the total emissions from short-haul flights by 3.
            """

            total_emissions_flight = total_short_haul_distance * 246

            total_emissions_train = total_emissions_flight / 3

            co2_reductions = (total_emissions_flight - total_emissions_train) / 1000

            plt.annotate(
                f"Total short-haul flights: {short_haul_count}\nTotal short-haul distance: {total_short_haul_distance:.2f} km\nCarbon emissions potential reductions: {round(co2_reductions,2)} kg of CO2",
                xy=(0.07, 1.2),
                xycoords="axes fraction",
                fontsize=12,
                backgroundcolor="white",
            )

            plt.title(f"All flights from {country}")
            plt.legend()
            plt.show()

    def aircrafts(self):
        """
        Plot a list of aircraft models from the airplanes_df DataFrame.

        This method prints the column names in airplanes_df and then
        prints a list of aircraft models.
        """

        column_names = self.airplanes_df.columns
        print("Column names in airplanes_df:", column_names)

        aircraft_models = self.airplanes_df["Name"].tolist()
        print("List of Aircraft Models:")
        for model in aircraft_models:
            print(model)

    def aircraft_info(self, aircraft_name):
        """
        Plot the information about aircaft name.

        Parameters:
        ---------------
            aircraft_name (str): The name of the aircraft for which
            information is to be retrieved.

        Returns:
        ---------------
            None. The method directly prints the retrieved information
            or suggestions to the console.
        """

        aircraft_models = self.airplanes_df["Name"].tolist()

        if aircraft_name in aircraft_models:
            query = f"Aircraft Information for {aircraft_name}:"
            query += f"\nName: {aircraft_name}"
            query += f"\nIATA code: {self.airplanes_df.loc[self.airplanes_df['Name'] == aircraft_name, 'IATA code'].iloc[0]}"
            query += f"\nICAO code: {self.airplanes_df.loc[self.airplanes_df['Name'] == aircraft_name, 'ICAO code'].iloc[0]}"

            llm = ChatOpenAI(temperature=0.1)

            result = llm.invoke(query)

            print(result.content)

        else:
            close_matches = get_close_matches(
                aircraft_name, aircraft_models, n=5, cutoff=0.3
            )
            if close_matches:
                print(f"Aircraft '{aircraft_name}' not found. Did you mean:")
                for match in close_matches:
                    print(f"- {match}")
            else:
                print(f"No close matches found for '{aircraft_name}'.")

                all_aircraft_names = self.airplanes_df["Name"].tolist()
                random.shuffle(all_aircraft_names)

                recommended_list = all_aircraft_names[:5]
                print("Here are some recommended aircraft names to choose from:")
                for recommend in recommended_list:
                    print(f"- {recommend}")

    def airport_info(self, airport_name):
        """
        Plot the information about airport name.

        Parameters:
        ---------------
            airport_name (str): The name of the airport for which
            information is to be retrieved.

        Returns:
        ---------------
            None. The method directly prints the retrieved information
            or suggestions to the console.
        """

        airport_models = self.merge_df["Name"].tolist()

        if airport_name in airport_models:
            print(f"Airport Information for {airport_name}:")

            query = f"Provide details for the airport named {airport_name}. Include information such as Airport ID, Source airport, City, Latitude, and Longitude."

            llm = ChatOpenAI(temperature=0.1)

            result = llm.invoke(query)

            print(result.content)
        else:
            close_matches = get_close_matches(
                airport_name, airport_models, n=5, cutoff=0.3
            )
            if close_matches:
                print(f"Aircraft '{airport_name}' not found. Did you mean:")
                for match in close_matches:
                    print(f"- {match}")
            else:
                print(f"No close matches found for '{airport_name}'.")

                all_airport_names = self.merge_df["Name"].tolist()
                random.shuffle(all_airport_names)

                recommended_list = all_airport_names[:5]
                print("Here are some recommended aircraft names to choose from:")
                for recommend in recommended_list:
                    print(f"- {recommend}")
