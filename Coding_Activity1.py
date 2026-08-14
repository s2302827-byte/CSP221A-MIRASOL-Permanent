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


def log_action(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        logging.info(f"{self.name}: starting {func.__name__}")
        result = func(self, *args, **kwargs)
        logging.info(f"{self.name}: finished {func.__name__}")
        return result
    return wrapper


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



def fleet_report(robots):
    for robot in robots:
        print(str(robot))



def run_task_safely(robot, **kwargs):
    try:
        result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as exc:
        logging.error(str(exc))
    else:
        print(f"Result: {result}")
    finally:
        print(f"{robot.name} battery now {robot.battery}%.")


class Buggy:
    items = []  # shared by every instance -- the bug
 
    def add(self, x):
        self.items.append(x)
 
 
class Fixed:
    def __init__(self):
        self.items = []  # each instance gets its own list -- the fix
 
    def add(self, x):
        self.items.append(x)


if __name__ == "__main__":
    roomba = CleaningRobot("Roomba", dust_capacity=2.0)
    drone = DroneRobot.from_config({"name": "Aqua-Drone", "battery": 15})
 
    fleet_report([roomba, drone])
    run_task_safely(roomba)   
    run_task_safely(drone)    



    a, b = Buggy(), Buggy()
    a.add(1)
    b.add(2)
    print("Buggy shared list:", a.items, b.items, a.items is b.items)
 
    c, d = Fixed(), Fixed()
    c.add(1)
    d.add(2)
    print("Fixed separate lists:", c.items, d.items, c.items is d.items)