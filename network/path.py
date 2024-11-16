import heapq
from network.graph import NeighbourGraphBuilder

class PathFinder:
    """
    Task 3: Complete the definition of the PathFinder class by:
    - completing the definition of the __init__() method (if needed)
    - completing the "get_shortest_path()" method (don't hesitate to divide 
      your code into several sub-methods)
    """

    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap

        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)


    def find_station_by_name(self, station_name):
        """Helper method to find a station object by its name."""
        for station in self.tubemap.stations.values():  # Iterate over dictionary values (Station objects)
            if station.name == station_name:
                return station
        return None
    

    def find_station_by_id(self, station_id):
        """Helper method to find a station object by its ID."""
        if station_id in self.tubemap.stations:
            return self.tubemap.stations[station_id]
        return None
            
        
    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path from start_station_name to end_station_name.
        
        The shortest path is the path that takes the least amount of time.

        For instance, get_shortest_path('Stockwell', 'South Kensington') 
        should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}), 
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.
        
        You can use the Dijkstra algorithm to find the shortest path from
        start_station_name to end_station_name.

        Find a tutorial on YouTube to understand how the algorithm works, 
        e.g. https://www.youtube.com/watch?v=GazC3A4OQTE
        
        Alternatively, find the pseudocode on Wikipedia: https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not 
                exist.
                Returns a list with one Station object (the station itself) if 
                start_station_name and end_station_name are the same.
        """
        # Retrieve start and end stations by name
        start_station = self.find_station_by_name(start_station_name)
        end_station = self.find_station_by_name(end_station_name)

        if not start_station or not end_station:
            return None
        
        # If start and end stations are the same, return the station itself
        if start_station == end_station:
            return [start_station]
        
        # Initialize Dijkstra's algorithm
        ## All distances are initialized to infinity
        distances = {station.id: float('inf') for station in self.tubemap.stations.values()}

        ## The distance from the start station to itself is None
        previous = {station.id: None for station in self.tubemap.stations.values()}

        ## The distance from the start station to itself is 0
        distances[start_station.id] = 0
        
        ## Initialize the priority queue with the start station
        priority_queue = [(0, start_station.id)]
        heapq.heapify(priority_queue)
        
        # Run Dijkstra's algorithm 
        ## Stop when priority_queue is empty
        while priority_queue:
            current_distance, current_station_id = heapq.heappop(priority_queue)

            # Stop if we reached the destination
            if current_station_id == end_station.id:
                break
            
            # Iterate over every neighbors
            for neighbor_id, connections in self.graph.get(current_station_id, {}).items():
                # Find shortest connection time between all neighbors
                total_time = min(conn.time for conn in connections)
                # Add the connection time to the current distance 
                new_distance = current_distance + total_time
                
                # If the new distance is shorter than the previous distance
                if new_distance < distances[neighbor_id]:
                    # Update the distance to the neighbor and the previous station
                    distances[neighbor_id] = new_distance
                    previous[neighbor_id] = current_station_id
                    # Add the neighbor to the priority queue
                    heapq.heappush(priority_queue, (new_distance, neighbor_id))
        
        # Reconstruct the path
        path = []
        current_id = end_station.id
        # Reconstruct the path by following the previous station
        while current_id is not None:
            # Insert the station at the beginning of the path
            path.insert(0, self.find_station_by_id(current_id))
            current_id = previous[current_id]
        
        # If path reconstruction failed (no valid path)
        if path[0] != start_station:
            return None
        
        return path


def test_shortest_path():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    path_finder = PathFinder(tubemap)

    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
    
    station_names = [station.name for station in stations]
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
                "Green Park"]
    
    assert station_names == expected

if __name__ == "__main__":
    test_shortest_path()
