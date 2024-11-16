import json
import math
from .components import Station, Line, Connection

class TubeMap:
    """
    Task 1: Complete the definition of the TubeMap class by:
    - completing the "import_from_json()" method

    Don't hesitate to divide your code into several sub-methods, if needed.

    As a minimum, the TubeMap class must contain these three member attributes:
    - stations: a dictionary that indexes Station instances by their id 
      (key=id (str), value=Station)
    - lines: a dictionary that indexes Line instances by their id 
      (key=id, value=Line)
    - connections: a list of Connection instances for the TubeMap 
      (list of Connections)
    """

    def __init__(self):
        self.stations = {}  # key: id (str), value: Station instance
        self.lines = {}  # key: id (str), value: Line instance
        self.connections = []  # list of Connection instances


    def import_from_json(self, filepath):
        """ Import tube map information from a JSON file.
        
        During the import process, the `stations`, `lines` and `connections` 
        attributes should be updated.

        You can use the `json` python package to easily load the JSON file at 
        `filepath`

        Note: when the indicated zone is not an integer (for instance: "2.5"), 
            it means that the station belongs to two zones. 
            For example, if the zone of a station is "2.5", 
            it means that the station is in both zones 2 and 3.

        Args:
            filepath (str) : relative or absolute path to the JSON file 
                containing all the information about the tube map graph to 
                import. If filepath is invalid, no attribute should be updated, 
                and no error should be raised.

        Returns:
            None
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            # Process the data only if it is a valid, non-empty dictionary
            if isinstance(data, dict) and data:
                self.import_stations(data.get('stations', []))
                self.import_lines(data.get('lines', []))
                self.import_connections(data.get('connections', []))

        except (FileNotFoundError, json.JSONDecodeError):
            # If file is not found or invalid JSON, just return without updating
            return
    

    def import_stations(self, stations_data):

        for station_info in stations_data:  # Iterate over the list directly

            station_id = station_info.get('id')  # Get station_id from each dictionary
            
            # Check for zone that are ".5" and split into two zones
            zone = station_info.get('zone')

            # Initialize an empty set to hold zones
            zones = set()

            if isinstance(zone, str) and '.' in zone:
                lower_zone, upper_zone = math.floor(float(zone)), math.ceil(float(zone))
                # Add both the lower and upper bounds to the zones set
                zones.add(lower_zone)
                zones.add(upper_zone)
            else:
                # Convert to an integer and add it to the zones set
                zones.add(int(zone))
            
            # Create Station instance (assuming Station class is defined)
            station = Station(
                id=str(station_id),
                name=str(station_info.get('name')),
                zones=zones,
            )
            self.stations[str(station_id)] = station


    def import_lines(self, lines_data):

        for line_info in lines_data:
            # Get the Line ID and name
            line_id = line_info.get('line')
            line_name = line_info.get('name')

            # Create Line instance
            line = Line(
                id=line_id,
                name=line_name,
            )
            self.lines[line_id] = line


    def import_connections(self, connections_data):

        for connection_info in connections_data:
            # Get the station objects from the station IDs
            station1 = self.stations.get(str(connection_info['station1']))
            station2 = self.stations.get(str(connection_info['station2']))
            line = self.lines.get(str(connection_info.get('line')))
            time=int(connection_info.get('time'))

            if station1 and station2 and line:  # Ensure all objects exist
                # Create Connection instance
                connection = Connection(
                    stations={station1, station2},  # Pass as a set
                    line=line,  # Pass the Line object
                    time=time,  # Ensure time is an int
                )
                self.connections.append(connection)


def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    print("Number of stations:", len(tubemap.stations))
    print("Number of lines:", len(tubemap.lines))
    print("Number of connections:", len(tubemap.connections))

    print("\nSome examples:")
    
    # view one example Station
    print(tubemap.stations[list(tubemap.stations)[10]])
    
    # view one example Line
    print(tubemap.lines[list(tubemap.lines)[0]])
    
    # view the first Connection
    print(tubemap.connections[0])
    
    # view stations for the first Connection
    print([station for station in tubemap.connections[0].stations])

if __name__ == "__main__":
    test_import()
