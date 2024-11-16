import unittest
import os
import json
import shutil
from tube.map import TubeMap
from network.graph import NeighbourGraphBuilder, calculate_total_connections


class TestGraph(unittest.TestCase):

    def create_json_file(self, filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f)


    # Set up the test case
    def setUp(self):
        
        self.tubemap = TubeMap()
        self.graph_builder = NeighbourGraphBuilder()
        
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


    # Test the case where the input data is valid 
    def test_valid_graph(self):
        
        self.tubemap.import_from_json(self.valid_json_filepath)
        self.graph = self.graph_builder.build(self.tubemap)

        self.assertIsInstance(self.graph, dict, f"Graph {self.graph} is not a dict.")
        self.assertTrue(self.graph, "Graph is empty.")
        self.assertEqual(len(self.graph), 302, "Graph does not contain 302 stations.")
        connections_nbr = calculate_total_connections(self.graph)
        self.assertEqual(connections_nbr, 406, "Graph does not contain 406 connections.")

        self.assertEqual(self.graph['236']['99'],self.graph['99']['236'], "South Kensington and Gloucester Road are not connected.")
        self.assertEqual(self.graph['236']['99'][0].time, self.graph['99']['236'][0].time, "South Kensington and Gloucester Road have different times.")
        self.assertEqual(self.graph['236']['99'][0].line.name, self.graph['99']['236'][0].line.name, "South Kensington and Gloucester Road are connected by different lines.")
        self.assertEqual(self.graph['236']['99'][0].stations, self.graph['99']['236'][0].stations, "South Kensington and Gloucester Road are connected by different stations.")

        self.assertEqual(self.graph["11"]["163"], self.graph["163"]["11"], "Baker Street and Marylebone are not connected.")
        self.assertEqual(self.graph["11"]["163"][0].time, self.graph["163"]["11"][0].time, "Baker Street and Marylebone have different times.")
        self.assertEqual(self.graph["11"]["163"][0].line.name, self.graph["163"]["11"][0].line.name, "Baker Street and Marylebone are connected by different lines.")
        self.assertEqual(self.graph["11"]["163"][0].stations, self.graph["163"]["11"][0].stations, "Baker Street and Marylebone are connected by different stations.")


    # Test the case where the input data is invalid
    def test_invalid_graph(self):
        
        self.tubemap.import_from_json(self.invalid_json_filepath)
        self.graph = self.graph_builder.build(self.tubemap)

        self.assertIsInstance(self.graph, dict, f"Graph {self.graph} is not a dict.")
        self.assertFalse(self.graph, "Graph is not empty.")
        self.assertEqual(self.graph, {}, "Graph should be empty when lines and connections are missing.")
    

    # Test the case where the input data is empty
    def test_empty_graph(self):
        
        self.tubemap.import_from_json(self.empty_json_filepath)
        self.graph = self.graph_builder.build(self.tubemap)

        self.assertIsInstance(self.graph, dict, f"Graph {self.graph} is not a dict.")
        self.assertFalse(self.graph, "Graph is not empty.")
        self.assertEqual(self.graph, {}, "Graph should be empty when lines and connections are missing.")


    # Test the case where the input data is incorrect
    def test_incorrect_graph(self):
        
        self.tubemap.import_from_json(self.incorrect_json_filepath)
        self.graph = self.graph_builder.build(self.tubemap)

        self.assertIsInstance(self.graph, dict, f"Graph {self.graph} is not a dict.")
        self.assertFalse(self.graph, "Graph is not empty.")
        self.assertEqual(self.graph, {}, "Graph should be empty when lines and connections are missing.")


    # Test the case where the input data is missing lines
    def test_missing_lines_graph(self):
        
        self.tubemap.import_from_json(self.missing_lines_filepath)
        self.graph = self.graph_builder.build(self.tubemap)

        self.assertIsInstance(self.graph, dict, f"Graph {self.graph} is not a dict.")
        self.assertFalse(self.graph, "Graph is not empty.")
        self.assertEqual(self.graph, {}, "Graph should be empty when lines and connections are missing.")


    # Test the case where the input data is missing stations
    def test_missing_stations_graph(self):
        
        self.tubemap.import_from_json(self.missing_stations_filepath)
        self.graph = self.graph_builder.build(self.tubemap)

        self.assertIsInstance(self.graph, dict, f"Graph {self.graph} is not a dict.")
        self.assertFalse(self.graph, "Graph is not empty.")
        self.assertEqual(self.graph, {}, "Graph should be empty when lines and connections are missing.")


    # Test the case where the input data is missing connections
    def test_missing_connections_graph(self):
        
        self.tubemap.import_from_json(self.missing_connections_filepath)
        self.graph = self.graph_builder.build(self.tubemap)

        self.assertIsInstance(self.graph, dict, f"Graph {self.graph} is not a dict.")
        self.assertFalse(self.graph, "Graph is not empty.")
        self.assertEqual(self.graph, {}, "Graph should be empty when lines and connections are missing.")



    # Test the case where the input data is missing two
    def test_missing_two_graph(self):
        
        self.tubemap.import_from_json(self.missing_two_filepath)
        self.graph = self.graph_builder.build(self.tubemap)

        self.assertIsInstance(self.graph, dict, f"Graph {self.graph} is not a dict.")
        self.assertFalse(self.graph, "Graph is not empty.")
        self.assertEqual(self.graph, {}, "Graph should be empty when lines and connections are missing.")


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