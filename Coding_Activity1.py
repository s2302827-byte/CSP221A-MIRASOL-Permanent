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