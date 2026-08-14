import abc
import functools
import logging
 
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class InsufficientBatteryError(Exception):
    def __init__(self, name, required, available):
        super().__init__(f"{name} needs {required}% battery for this task but only has {available}%.")

class Robot(abc.ABC):
    manufacturer = "Acme Robotics"
    population = 0
 
    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1
 
    @property
    def battery(self):
        return self._battery
 
    @battery.setter
    def battery(self, value):
        self._battery = max(0, min(100, value))
 
    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"
 
    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r}, battery={self.battery!r})"
 
    @abc.abstractmethod
    def perform_task(self, **kwargs):
        pass

    def use_battery(self, amount):
        if amount > self.battery:
            raise InsufficientBatteryError(self.name, amount, self.battery)
        self.battery -= amount


    @classmethod
    def from_config(cls, config):
        return cls(**config)



class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=1.5):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity
 
    @log_action
    def perform_task(self, **kwargs):
        self.use_battery(10)
        return f"{self.name} vacuumed a room."
 
 
class DroneRobot(Robot):
    def __init__(self, name, battery=100, max_altitude=120):
        super().__init__(name, battery)
        self.max_altitude = max_altitude
 
    def perform_task(self, **kwargs):
        self.use_battery(25)
        return f"{self.name} flew at {self.max_altitude}m."