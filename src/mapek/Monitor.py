from mapek.Knowledge import Knowledge
from mapek.Analyzer import Analyzer
from mapek.Observer import Observer
from mapek.Component import Component

class Monitor(Observer, Component):
    """
    The MAPE-K loop monitor component.
    
    Attributes:
        analyzer (Analyzer): The analyzer component of the MAPE-K loop
    """

    def __init__(self, analyzer: Analyzer):
        """
        Initializes the MAPE-K loop monitor with the analyzer.
        
        Args:
            analyzer (Analyzer): The analyzer component of the MAPE-K loop
        """

        self.analyzer = analyzer

    def update(self, distances: list, speeds: list, locations: list):
        """
        Sends a copy of the distances and speeds to be executed on
        
        Args:
            distances (list): List of distances from the sensors for each relevant ACV
            speeds (list): List of  speeds for each relevant ACV
        """

        self.execute(distances.copy(), speeds.copy(), locations.copy())

    def execute(self, distances: list, speeds: list, locations: list):
        """
        Updates knowledge with speeds and sends the distances and speeds to the analyzer
        
        Args:
            distances (list): List of distances from the sensors for each relevant ACV
            starting_speeds (list): List of starting speeds for each relevant ACV
        """

        knowledge = Knowledge()
        knowledge.starting_speeds = speeds
        knowledge.locations = locations

        self.analyzer.execute(distances)
        