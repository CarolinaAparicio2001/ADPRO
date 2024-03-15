# standard libraries
import os
# from io import BytesIO
from zipfile import ZipFile
import requests
##
# Third-party libraries
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, MultiPoint
from plotnine import ggplot, aes, geom_histogram, theme_minimal, scale_fill_manual
from IPython.display import display, HTML
from langchain_openai import ChatOpenAI
import langchain

# Local application libraries
from distance_airports import distance_geo


class Airplane:
    """
    A class to download airplane data and perform analysis on it.
    """

    def __init__(self):
        self.airlines_df = pd.DataFrame()
        self.airplanes_df = pd.DataFrame()
        self.airports_df = pd.DataFrame()
        self.routes_df = pd.DataFrame()
        self.merge_df = pd.DataFrame()

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

        """
        Check if the zip file was already downloaded
        """
        if not os.path.exists(zip_file_path):
            response = requests.get(
                "https://gitlab.com/adpro1/adpro2024/-/"
                "raw/main/Files/flight_data.zip?inline=false",
                stream=True,
            )
            """
            Ensure the request is successful
            """
            if response.status_code == 200:
                with open(zip_file_path, "wb") as f:
                    f.write(response.content)

        """
        Extract files if the zip file is downloaded
        """
        if os.path.exists(zip_file_path):
            extraction_dir = os.path.join(os.getcwd(), downloads_dir)
            with ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(downloads_dir)

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

    def merge_datasets(self) -> pd.DataFrame:
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
        # Drop the columns that I dont need
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

        # Assign the resulting merge_df to the instance variable
        self.merge_df = merge_df

        # print("Merge DataFrame:\n", self.merge_df.head())

        return self.merge_df

    def plot_airports_in_country(self, country):
        """
        Plot airports within the chosen country and use the ICAOs as legends.

        Parameters:
        - country (str): The name of the country where airports are to be plotted.
        """
        # Filter airports by the specified country
        country_airports = self.merge_df[self.merge_df["Source country"] == country]

        # Exit if no airports are found in the country
        if country_airports.empty:
            print(f"No airports found in {country}.")
            return

        # Load a map of the world
        world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

        # Filter the map to only include the specified country
        country_map = world[world["name"] == country]

        # Exit if the country is not found in the map dataset
        if country_map.empty:
            print(f"Country '{country}' not found.")
            return

        # Convert the filtered airports data into a GeoDataFrame
        gdf_airports = gpd.GeoDataFrame(
            country_airports,
            geometry=gpd.points_from_xy(
                country_airports.Longitude, country_airports.Latitude
            ),
        )

        # Plotting
        _, axis = plt.subplots(figsize=(10, 10))
        country_map.plot(ax=axis, color="lightgrey")
        gdf_airports.plot(ax=axis, marker="o", color="red", markersize=5)

        # Annotate each airport with its ICAO code
        for _, row in gdf_airports.iterrows():
            axis.text(row.geometry.x, row.geometry.y, row["ICAO"], fontsize=8)

        plt.title(f"Airports in {country}")
        plt.show()

    def distance_analysis(self):
        """
        Performs distance analysis between source and destination airports.
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

        self.merge_df["distance"].head()

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
        Plots flight routes originating from a specified airport. If the 'internal' parameter
        is set to True, it will display only domestic flights within the specified airport's country.
        Otherwise, it displays all flights from the airport on a global map.

        Parameters:
        - code_airport (str): IATA code of the source airport.
        - internal (bool): Flag for plotting only domestic flights; defaults to False.
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

        all_points = MultiPoint(list(source_points) + list(destination_points))

        gdf_flights = gpd.GeoDataFrame(flights, geometry=source_points)
        gdf_destinations = gpd.GeoDataFrame(flights, geometry=destination_points)

        _, axis = plt.subplots(figsize=(10, 10))

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
        Plot the most used airplane models based on the number of routes.

        Parameters:
            n (int): Number of airplane models to plot, that by default is 5.
            countries (str): Specific country or list of countries to consider, by default is None.
        """
        if countries is None:
            # Plot most used planes by route using the entire dataset
            top_airplanes = self.merge_df["Equipment"].value_counts().nlargest(n)
        else:
            # Plot most used planes by route for a specific country or list of countries
            if isinstance(countries, str):
                countries = [countries]

            filtered_routes = self.merge_df[
                self.merge_df["Source country"].isin(countries)
            ]
            top_airplanes = filtered_routes["Equipment"].value_counts().nlargest(n)

        top_airplanes.plot(
            kind="bar", title=f"Top {n} Airplane Models by Number of Routes"
        )
        plt.xlabel("Airplane Model")
        plt.ylabel("Number of Routes")
        plt.show()

    def plot_flights_by_country(self, country, internal=False, cutoff_distance=500):
        """
        Plot the map flight routes between domestic and international flights from source to destination airports.

        Parameters:
            country (str): Name of the source country.
            internal (bool): If the flight is internal or not. Being by default False.
            cutoff_distance (float): Threshold in km to differentiate between short-haul and long-haul flights.
        """

        # Ensure the distance column is available
        if "distance" not in self.merge_df.columns:
            self.distance_analysis()  # Compute distances if not already done

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

            # Annotate total information about short-haul flights
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

            # This section assumes that the plotting for non-internal (all routes) does not differentiate by distance
            # Extend this logic if you wish to categorize all flights by distance as well.

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

            # This section compares the potential carbon emission reductions between short-haul flights and equivalent train rides.

            # Supposing that a domestic flight emits 246 grams per kilometer, calculate the total kilometer of short-haul flights times 246
            total_emissions_flight = total_short_haul_distance * 246

            # Next, we consider the environmental impact of short-haul flights compared to train rides.
            # Research indicates that short-haul flights covering a distance of less than 500 km can produce three times more CO2 emissions than a train ride over the same distance.
            # Hence, to estimate the emissions from equivalent train rides, we divide the total emissions from short-haul flights by 3.
            total_emissions_train = total_emissions_flight / 3

            # Shows potential carbon reduction by favoring trains over short-haul flights.
            co2_reductions = (total_emissions_flight - total_emissions_train) / 1000

            # Annotate total information about short-haul flights
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

        This method prints the column names in airplanes_df and then prints a list of aircraft models.
        """
        column_names = self.airplanes_df.columns
        print("Column names in airplanes_df:", column_names)
        # Assuming 'Name' is the column containing aircraft models in self.airplane_df
        aircraft_models = self.airplanes_df["Name"].tolist()
        print("List of Aircraft Models:")
        for model in aircraft_models:
            print(model)

    def aircraft_info(self, aircraft_name):
        """
        Plot the information about aircaft name.

        Parameters:
            aircraft_name (str): The name of the aircraft for which information is to be retrieved.
        """
        aircraft_models = self.airplanes_df["Name"].tolist()

        # Check if the provided aircraft_name is in the list
        if aircraft_name in aircraft_models:
            # Retrieve information for the specified aircraft_name
            query = f"Aircraft Information for {aircraft_name}:"
            query += f"\nName: {aircraft_name}"
            query += f"\nIATA code: {self.airplanes_df.loc[self.airplanes_df['Name'] == aircraft_name, 'IATA code'].iloc[0]}"
            query += f"\nICAO code: {self.airplanes_df.loc[self.airplanes_df['Name'] == aircraft_name, 'ICAO code'].iloc[0]}"

            # Create an instance of ChatOpenAI with a low temperature for focused responses
            llm = ChatOpenAI(temperature=0.1)

            # Invoke the LLM with the query
            result = llm.invoke(query)

            # Print the LLM-generated content as a Markdown table
            print(result.content)

        else:
            # Attempt to find close matches
            close_matches = get_close_matches(
                aircraft_name, aircraft_models, n=5, cutoff=0.3
            )
            if close_matches:
                print(f"Aircraft '{aircraft_name}' not found. Did you mean:")
                for match in close_matches:
                    print(f"- {match}")
            else:
                # If no close matches found, suggest a generic list of recommended aircraft names
                print(f"No close matches found for '{aircraft_name}'.")

                # Shuffle the list of aircraft names to ensure a different subset is selected each time
                all_aircraft_names = self.airplanes_df["Name"].tolist()
                random.shuffle(all_aircraft_names)  # Shuffle the list in place

                # Select the top 5 (or however many you prefer) from the shuffled list
                recommended_list = all_aircraft_names[:5]
                print("Here are some recommended aircraft names to choose from:")
                for recommend in recommended_list:
                    print(f"- {recommend}")

    def airport_info(self, airport_name):
        """
        Plot the information about airport name.

        Parameters:
            airport_name (str): The name of the airport for which information is to be retrieved.
        """
        airport_models = self.merge_df["Name"].tolist()

        if airport_name in airport_models:
            # Retrieve information for the specified airport_name
            unique_info = self.merge_df[self.merge_df["Name"] == airport_name][
                [
                    "Airport ID",
                    "Name",
                    "Source airport",
                    "City",
                    "latitude_source",
                    "longitude_source",
                ]
            ].drop_duplicates(subset=["Name"])
            print(f"Airport Information for {airport_name}:")
            # print(unique_info.to_string(index=False))

            # Construct a query for the language model
            query = f"Provide details for the airport named {airport_name}. Include information such as Airport ID, Source airport, City, Latitude, and Longitude."

            # Create an instance of ChatOpenAI with a low temperature for focused responses
            llm = ChatOpenAI(temperature=0.1)

            # Invoke the LLM with the query
            result = llm.invoke(query)

            # Print the LLM-generated content as a Markdown table
            print(result.content)
        else:
            # Attempt to find close matches
            close_matches = get_close_matches(
                airport_name, airport_models, n=5, cutoff=0.3
            )
            if close_matches:
                print(f"Aircraft '{airport_name}' not found. Did you mean:")
                for match in close_matches:
                    print(f"- {match}")
            else:
                # If no close matches found, suggest a generic list of recommended aircraft names
                print(f"No close matches found for '{airport_name}'.")

                # Shuffle the list of aircraft names to ensure a different subset is selected each time
                all_airport_names = self.merge_df["Name"].tolist()
                random.shuffle(all_airport_names)  # Shuffle the list in place

                # Select the top 5 (or however many you prefer) from the shuffled list
                recommended_list = all_airport_names[:5]
                print("Here are some recommended aircraft names to choose from:")
                for recommend in recommended_list:
                    print(f"- {recommend}")
