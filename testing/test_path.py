import unittest
import os
import json
import shutil
from tube.map import TubeMap
from network.path import PathFinder

class TestPath(unittest.TestCase):

    def create_json_file(self, filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f)


    # Set up the test case
    def setUp(self):
        
        self.tubemap = TubeMap()
        
        # Define paths to the real and test JSON files
        self.data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        self.original_json_filepath = os.path.join(self.data_directory, 'london.json')
        self.valid_json_filepath = os.path.join(self.data_directory, 'london_test.json')
        self.invalid_json_filepath = os.path.join(self.data_directory, 'invalid.json')
        self.incorrect_json_filepath = os.path.join(self.data_directory, 'incorrect.txt')
        self.empty_json_filepath = os.path.join(self.data_directory, 'empty.json')
        self.missing_lines_filepath = os.path.join(self.data_directory, 'missing_lines.json')
        self.missing_stations_filepath = os.path.join(self.data_directory, 'missing_stations.json')
        self.missing_connections_filepath = os.path.join(self.data_directory, 'missing_connections.json')
        self.missing_two_filepath = os.path.join(self.data_directory, 'missing_two.json')

        # Ensure the original JSON file exists before copying
        if os.path.exists(self.original_json_filepath):
            # Copy the original london.json file to london_test.json for testing
            shutil.copy(self.original_json_filepath, self.valid_json_filepath)
        else:
            raise FileNotFoundError(f"The original file {self.original_json_filepath} does not exist.")

        # Create an empty JSON file for the empty test case
        with open(self.empty_json_filepath, 'w') as f:
            json.dump({}, f)

        # Create an empty text file
        with open(self.incorrect_json_filepath, 'w') as f:
            pass  # Just create an empty file

        # Create JSON file with connections and stations, but no lines
        self.create_json_file(self.missing_lines_filepath, {
            "stations": [
                {"id": "1", "name": "Station A", "zone": "1"},
                {"id": "2", "name": "Station B", "zone": "2"}
            ],
            "connections": [
                {"station1": "1", "station2": "2", "line": "1", "time": "5"},
                {"station1": "2", "station2": "4", "line": "1", "time": "4"}
            ]
        })

        # Create JSON file with lines and connections, but no stations
        self.create_json_file(self.missing_stations_filepath, {
            "lines": [
                {"id": "1", "name": "Line A"}
            ],
            "connections": [
                {"station1": "1", "station2": "2", "line": "1", "time": "5"}
            ]
        })

        # Create JSON file with stations and lines, but no connections
        self.create_json_file(self.missing_connections_filepath, {
            "stations": [
                {"id": "1", "name": "Station A", "zone": "1"},
                {"id": "2", "name": "Station B", "zone": "2"}
            ],
            "lines": [
                {"id": "1", "name": "Line A"}
            ],
        })

        # Create JSON file with neither lines, nor connections
        self.create_json_file(self.missing_two_filepath, {
            "stations": [
                {"id": "1", "name": "Station A", "zone": "1"},
                {"id": "2", "name": "Station B", "zone": "2"}
            ],
        })

    # Test valid JSON file
    def test_valid_shortest_path(self):
        self.tubemap.import_from_json(self.valid_json_filepath)
        path_finder = PathFinder(self.tubemap)
        stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
        station_names = [station.name for station in stations]
        self.assertEqual(station_names, ['Covent Garden', 'Leicester Square', 'Piccadilly Circus', 'Green Park'])
        
        stations = path_finder.get_shortest_path("Clapham South", "South Kensington")
        station_names = [station.name for station in stations]
        self.assertEqual(station_names, ['Clapham South', 'Clapham Common', 'Clapham North', 'Stockwell', 'Vauxhall', 'Pimlico', 'Victoria', 'Sloane Square', 'South Kensington'])

        stations = path_finder.get_shortest_path("Clapham South", "Clapham South")
        station_names = [station.name for station in stations]
        self.assertEqual(station_names, ['Clapham South'])

        stations = path_finder.get_shortest_path("Morden", "Wembley Central")
        station_names = [station.name for station in stations]
        real_shortest_path = ['Morden', 'South Wimbledon', 'Colliers Wood', 
                              'Tooting Broadway', 'Tooting Bec', 'Balham', 'Clapham South', 
                              'Clapham Common', 'Clapham North', 'Stockwell', 'Vauxhall', 
                              'Pimlico', 'Victoria', 'Green Park', 'Bond Street', 'Baker Street', 
                              'Marylebone', 'Edgware Road (B)', 'Paddington', 'Warwick Avenue',
                              'Maida Vale', 'Kilburn Park', "Queen's Park", 'Kensal Green',
                              'Willesden Junction', 'Harlesden', 'Stonebridge Park', 'Wembley Central']
        self.assertEqual(station_names, real_shortest_path)
    
    # Test invalid JSON file
    def test_invalid_json(self):
        self.tubemap.import_from_json(self.invalid_json_filepath)
        path_finder = PathFinder(self.tubemap)
        stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
        self.assertIsNone(stations)

    # Test empty JSON file
    def test_empty_json(self):
        self.tubemap.import_from_json(self.empty_json_filepath)
        path_finder = PathFinder(self.tubemap)
        stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
        self.assertIsNone(stations)

    # Test incorrect JSON file
    def test_incorrect_json(self):
        self.tubemap.import_from_json(self.incorrect_json_filepath)
        path_finder = PathFinder(self.tubemap)
        stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
        self.assertIsNone(stations)

    # Test missing lines JSON file
    def test_missing_lines_json(self):
        self.tubemap.import_from_json(self.missing_lines_filepath)
        path_finder = PathFinder(self.tubemap)
        stations = path_finder.get_shortest_path("Station A", "Station B")
        self.assertIsNone(stations)

    # Test missing stations JSON file
    def test_missing_stations_json(self):
        self.tubemap.import_from_json(self.missing_stations_filepath)
        path_finder = PathFinder(self.tubemap)
        stations = path_finder.get_shortest_path("Station A", "Station B")
        self.assertIsNone(stations)

    # Test missing connections JSON file
    def test_missing_connections_json(self):
        self.tubemap.import_from_json(self.missing_connections_filepath)
        path_finder = PathFinder(self.tubemap)
        stations = path_finder.get_shortest_path("Station A", "Station B")
        self.assertIsNone(stations)

    # Test missing two JSON file
    def test_missing_two_json(self):
        self.tubemap.import_from_json(self.missing_two_filepath)
        path_finder = PathFinder(self.tubemap)
        stations = path_finder.get_shortest_path("Station A", "Station B")
        self.assertIsNone(stations)

    
    # Clean up
    def tearDown(self):
        """Clean up by removing test JSON files."""
        # Remove the test JSON file
        if os.path.exists(self.valid_json_filepath):
            os.remove(self.valid_json_filepath)
        
        # Remove the empty JSON file
        if os.path.exists(self.empty_json_filepath):
            os.remove(self.empty_json_filepath)

        # Remove the incorrect JSON file
        if os.path.exists(self.incorrect_json_filepath):
            os.remove(self.incorrect_json_filepath)

        # Remove the missing lines JSON file
        if os.path.exists(self.missing_lines_filepath):
            os.remove(self.missing_lines_filepath)

        # Remove the missing stations JSON file
        if os.path.exists(self.missing_stations_filepath):
            os.remove(self.missing_stations_filepath)

        # Remove the missing connections JSON file
        if os.path.exists(self.missing_connections_filepath):
            os.remove(self.missing_connections_filepath)

        # Remove the missing two JSON file
        if os.path.exists(self.missing_two_filepath):
            os.remove(self.missing_two_filepath)


if __name__ == '__main__':
    unittest.main()