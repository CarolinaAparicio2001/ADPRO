"""
Module: TestDistanceGeo
Description: Tests for the distance_geo function from the distance_airports module.
""" 

import unittest
from geopy.distance import geodesic
from distance_airports import distance_geo

class TestDistanceGeo(unittest.TestCase):
    """A test suite for the distance_geo function."""

    def test_distance_geo_same_location(self):
        """Test the distance_geo function with the same location, should return 0."""
        # Used the GKA airport data
        distance = distance_geo(-6.081690,145.391998,-6.081690, 145.391998)
        self.assertEqual(distance, 0)

    def test_distance_geo_different_airports_same_country(self):
        """Test the distance_geo function with different airports in the same country."""
        # Calculate expected distance using geopy, between GKA and HGU both in Papua New Guinea
        expected_distance = geodesic((-6.081690,145.391998), (-5.826790,144.296005)).km
        distance = distance_geo(-6.081690,145.391998, -5.826790,144.296005)
        self.assertAlmostEqual(distance, expected_distance, places=5)

    def test_distance_geo_different_countries(self):
        """Test the distance_geo function with different airports in different countries."""
        # Calculate expected distance using geopy, GKA from Papua New Guinea and CPO in Chile
        expected_distance = geodesic((-6.081690,145.391998), (-27.261200,-70.779198)).km
        distance = distance_geo(-6.081690,145.391998, -27.261200,-70.779198)
        self.assertAlmostEqual(distance, expected_distance, places=5)

if __name__ == '__main__':
    unittest.main()
