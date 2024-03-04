import ipytest
ipytest.autoconfig()

import pytest
from distance_airports import distance_geo
from class_airplane import Airplane

class TestDistanceCalculator:
    @classmethod
    def setup_class(cls):
        """Set up method to initialize the Airplane class and download the merge dataset.
        """
        cls.processor = Airplane()
        cls.processor.download_data()
        cls.processor.merge_datasets()

    def select_airports(self, processor, same_country=True):
        """
        Selects a pair of airports based on whether they are in the same country or not.
        If in the same country, the same airport can be selected, and the distance will be 0.
        If in different countries, ensures they are different airports to have a valid distance calculation.
        """
        if same_country:
            airports = processor.merge_df[processor.merge_df['Source country'] == processor.merge_df['Destination country']]
            # Allow selecting the same airport for same-country distance (distance will be 0)
        else:
            airports = processor.merge_df[processor.merge_df['Source country'] != processor.merge_df['Destination country']]
            airports = airports[airports['Source airport ID'] != airports['Destination airport ID']]

        if airports.empty:
            return None
        else:
            return airports.iloc[0]

    def __call__(self):
        """Callable method to define tests."""
        self.test_distance_same_country()
        self.test_distance_different_countries()

    def test_distance_same_country(self):
        """Tests that the calculated distance between two airports in the same country is 0."""
        row = self.select_airports(self.processor, same_country=True)
        if row is not None:
            calculated_distance = distance_geo(row['latitude_source'], row['longitude_source'], row['latitude_destination'], row['longitude_destination'])
            assert calculated_distance == 0, f"The calculated distance should be 0 for airports in the same country. Got: {calculated_distance}"
        else:
            pytest.skip("No suitable data for same-country distance calculation found.")

    def test_distance_different_countries(self):
        """Tests that the calculated distance between two airports in different countries is greater than 0."""
        row = self.select_airports(self.processor, same_country=False)
        if row is not None:
            calculated_distance = distance_geo(row['latitude_source'], row['longitude_source'], row['latitude_destination'], row['longitude_destination'])
            assert calculated_distance > 0, "The calculated distance should be greater than 0 for airports in different countries."
        else:
            pytest.skip("No suitable data for different-countries distance calculation found.")

# Instead of unittest.main(), you use:
ipytest.run()