import subject

class ACV:
    """Represents an Autonomously Controlled Vehicle (ACV). Travels in one dimension.
    
    Attributes:
        index (int): The index of the ACV.
        location (float): The current location of the ACV.
        speed (float): The current speed of the ACV.
        distance (float): The distance between the ACV and the ACV in front of it.
        total_penalty (float): The total penalty incurred by the ACV.
        total_regret (float): The total regret of the ACV.
    """

    def __init__(self, index: int, start_location: float, start_speed: float):
        """
        Initializes the ACV with the given index, location, and speed.
        
        Args:
            index (int): The index of the ACV.
            start_location (float): The starting location of the ACV.
            start_speed (float): The starting speed of the ACV.
        """

        self.index = index
        self.location = start_location
        self.speed = start_speed  
        self.distance = 0
        self.total_penalty = 0
        self.total_regret = 0

    def update(self, speed_modifier, penalty, regret):
        """
        Updates the ACV's speed and location based on the given speed modifier.

        Args:
            speed_modifier (float): The speed modifier to apply to the ACV.
            penalty (float): The penalty incurred in this iteration
            regret (float): The regret incurred in this iteration
        """

        self.total_penalty += penalty
        self.total_regret += regret

        self.speed += speed_modifier
        self.speed = max(min(self.speed, subject.MAX_SPEED), -subject.MAX_SPEED)
        
        self.location += self.speed