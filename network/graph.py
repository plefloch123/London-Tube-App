from tube.map import TubeMap

class NeighbourGraphBuilder:
    """
    Task 2: Complete the definition of the NeighbourGraphBuilder class by:
    - completing the "build" method below (don't hesitate to divide your code 
      into several sub-methods, if needed)
    """

    def __init__(self):
        pass

    def build(self, tubemap):
        """ Builds a graph encoding neighbouring connections between stations.

        ----------------------------------------------

        The returned graph should be a dictionary having the following form:
        {
            "station_A_id": {
                "neighbour_station_1_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],

                "neighbour_station_2_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],
                ...
            }

            "station_B_id": {
                ...
            }

            ...

        }

        ----------------------------------------------

        For instance, knowing that the id of "Hammersmith" station is "110",
        graph['110'] should be equal to:
        {
            '17': [
                Connection(Hammersmith<->Barons Court, District Line, 1),
                Connection(Hammersmith<->Barons Court, Piccadilly Line, 2)
                ],

            '209': [
                Connection(Hammersmith<->Ravenscourt Park, District Line, 2)
                ],

            '101': [
                Connection(Goldhawk Road<->Hammersmith, Hammersmith & City Line, 2)
                ],

            '265': [
                Connection(Hammersmith<->Turnham Green, Piccadilly Line, 2)
                ]
        }

        ----------------------------------------------

        Args:
            tubemap (TubeMap) : tube map serving as a reference for building 
                the graph.

        Returns:
            graph (dict) : as described above. 
                If the input data (tubemap) is invalid, 
                the method should return an empty dict.
        """
        if not isinstance(tubemap, TubeMap):
            return {}

        graph = {}

        # Iterate over each connection in the TubeMap
        for connection in tubemap.connections:
            # Ensure the connection contains exactly two stations
            if len(connection.stations) != 2:
                continue  # Skip invalid connections

            # Unpack the two stations from the set
            station1, station2 = connection.stations

            # Get the IDs of the stations (assuming Station objects have an 'id' attribute)
            station1_id = station1.id
            station2_id = station2.id

            # Add station1 to graph if not already present
            if station1_id not in graph:
                graph[station1_id] = {}

            # Add station2 to graph if not already present
            if station2_id not in graph:
                graph[station2_id] = {}

            # If not already added, create a new entry for station2 in station1's dict
            if station2_id not in graph[station1_id]:
                graph[station1_id][station2_id] = []

            # Append the connection to the station1 -> station2 list
            graph[station1_id][station2_id].append(connection)

            # Since connections are bidirectional, we need to add station1 to station2's dict as well
            if station1_id not in graph[station2_id]:
                graph[station2_id][station1_id] = []

            # Append the connection to the station2 -> station1 list
            graph[station2_id][station1_id].append(connection)

        return graph


def calculate_total_connections(network: dict) -> int:
    total_connections = 0
    
    # Loop through each station in the network dictionary
    for station, adjacent_stations in network.items():
        # For each station, go through its adjacent stations
        for adjacent_station, routes in adjacent_stations.items():
            # Increase the connection count by the number of routes to the adjacent station
            total_connections += len(routes)
    
    # Divide by 2 to account for double counting (connections are bidirectional)
    total_connections //= 2
    
    return total_connections


def test_graph():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build(tubemap)

    print(graph)
    print("number of stations: ", len(graph))
    connection_nbr = calculate_total_connections(graph)
    print("number of connections: ", connection_nbr)

    # test South Kensington and Gloucester Road
    print(graph['236']['99'])
    print(graph['99']['236'])

if __name__ == "__main__":
    test_graph()
