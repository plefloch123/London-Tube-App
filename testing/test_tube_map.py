import unittest
import os
import json
import shutil
from tube.map import TubeMap

class TestTubeMap(unittest.TestCase):

    def create_json_file(self, filepath, data):
            with open(filepath, 'w') as f:
                json.dump(data, f)


    # Set up the test case
    def setUp(self):
        """Create a TubeMap instance before each test."""
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


    ### Big test cases when it works ###
    def test_import_valid_json(self):
        """Test that valid JSON data is correctly imported."""
        # Import from the test JSON file
        self.tubemap.import_from_json(self.valid_json_filepath)

        # Test stations
        self.assertEqual(len(self.tubemap.stations), 302)
        self.assertIsInstance(self.tubemap.stations, dict, f"Station {self.tubemap.stations} is not a dict.")

        for station_id in self.tubemap.stations.keys():  # If stations are stored in a dictionary
            self.assertIsInstance(station_id, str, f"Station ID {station_id} is not a string.")
        
        for station in self.tubemap.stations.values():
            self.assertIsInstance(station.name, str, f"Station name {station.name} is not a string.")
            self.assertIsInstance(station.zones, set, f"Station zones {station.zones} is not a set.")
            for zone in station.zones:
                self.assertIsInstance(zone, int, f"Zone {zone} is not an integer.")

        # Test lines
        self.assertEqual(len(self.tubemap.lines), 13)
        self.assertIsInstance(self.tubemap.lines, dict, f"Lines {self.tubemap.lines} is not a dict.")

        for line_id in self.tubemap.lines.keys():  # If lines are stored in a dictionary
            self.assertIsInstance(line_id, str, f"Line ID {line_id} is not a string.")

        for line in self.tubemap.lines.values():
            self.assertIsInstance(line.id, str, f"Line name {line.id} is not a string.")
            self.assertIsInstance(line.name, str, f"Line name {line.name} is not a string.")
        
        # Test connections
        self.assertEqual(len(self.tubemap.connections), 406)
        self.assertIsInstance(self.tubemap.connections, list, f"Connections {self.tubemap.connections} is not a list.")

        for connection in self.tubemap.connections:
            self.assertIsInstance(connection.stations, set, f"Connection stations {connection.stations} is not a set.")
            for station in connection.stations:
                self.assertIsInstance(station, type(station), f"Station {station} is not of {type(station)}.")
            self.assertIsInstance(connection.line, type(line), f"Connection line {connection.line} is not of {type(line)}.")
            self.assertIsInstance(connection.time, int, f"Connection time {connection.time} is not an integer.")


    ### Test cases when it fails ###
    # Test cases for invalid JSON files
    def test_import_invalid_filepath(self):
        # Attempt to import from an invalid path
        self.tubemap.import_from_json(self.invalid_json_filepath)

        # Ensure no stations, lines, or connections were imported
        self.assertEqual(len(self.tubemap.stations), 0)
        self.assertEqual(len(self.tubemap.lines), 0)
        self.assertEqual(len(self.tubemap.connections), 0)


    # Test cases for empty JSON files
    def test_import_empty_json(self):
        with open(self.empty_json_filepath, 'w') as f:
            json.dump({}, f)

        self.tubemap.import_from_json(self.empty_json_filepath)

        # Ensure no stations, lines, or connections were imported
        self.assertEqual(len(self.tubemap.stations), 0)
        self.assertEqual(len(self.tubemap.lines), 0)
        self.assertEqual(len(self.tubemap.connections), 0)


    # Test cases for incorrect file types (like txt file)
    def test_import_incorrect_filetype(self):
        self.tubemap.import_from_json(self.incorrect_json_filepath)

        # Ensure no stations, lines, or connections were imported
        self.assertEqual(len(self.tubemap.stations), 0)
        self.assertEqual(len(self.tubemap.lines), 0)
        self.assertEqual(len(self.tubemap.connections), 0)
    
    
    # Test cases for missing lines
    def test_import_missing_lines(self):
        self.tubemap.import_from_json(self.missing_lines_filepath)

        # Ensure no stations, lines, or connections were imported
        self.assertEqual(len(self.tubemap.stations), 2, f"Number of stations {len(self.tubemap.stations)} is not 2.")
        self.assertEqual(len(self.tubemap.lines), 0, f"Number of lines {len(self.tubemap.lines)} is not 13.")
        self.assertEqual(len(self.tubemap.connections), 0, f"Number of connections {len(self.tubemap.connections)} is not 0.")

    
    # Test cases for missing stations
    def test_import_missing_stations(self):
        self.tubemap.import_from_json(self.missing_stations_filepath)

        # Ensure no stations, lines, or connections were imported
        self.assertEqual(len(self.tubemap.stations), 0, f"Number of stations {len(self.tubemap.stations)} is not 2.")
        self.assertEqual(len(self.tubemap.lines), 1, f"Number of lines {len(self.tubemap.lines)} is not 1.")
        self.assertEqual(len(self.tubemap.connections), 0, f"Number of connections {len(self.tubemap.connections)} is not 0.")    
    
    
    # Test cases for missing connections
    def test_import_missing_connections(self):
        self.tubemap.import_from_json(self.missing_connections_filepath)

        # Ensure no stations, lines, or connections were imported
        self.assertEqual(len(self.tubemap.stations), 2, f"Number of stations {len(self.tubemap.stations)} is not 2.")
        self.assertEqual(len(self.tubemap.lines), 1, f"Number of lines {len(self.tubemap.lines)} is not 1.")
        self.assertEqual(len(self.tubemap.connections), 0)
    

    # Test cases for missing two (lines and connections) -> only stations
    def test_import_missing_two(self):
        self.tubemap.import_from_json(self.missing_two_filepath)

        # Ensure no stations, lines, or connections were imported
        self.assertEqual(len(self.tubemap.stations), 2, f"Number of stations {len(self.tubemap.stations)} is not 0.")
        self.assertEqual(len(self.tubemap.lines), 0, f"Number of lines {len(self.tubemap.lines)} is not 0.")
        self.assertEqual(len(self.tubemap.connections), 0, f"Number of connections {len(self.tubemap.connections)} is not 0.")
                                                                                        

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