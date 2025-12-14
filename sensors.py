import random
import time

class Sensor:
    def __init__(self, name, room, value=0):
        self.name = name
        self.room = room
        self.value = value

    def read_value(self):
        return f"{self.name} in {self.room}: {self.value}"   
    
    def update_value(self, new_value):
        self.value = new_value

    
class TemperatureSensor(Sensor):
    def __init__(self, name, room, value=0):
        super().__init__(name, room, value)
        self.unit = "°C"

    def read_value(self):
        return f"Temperature in {self.room}: {self.value} {self.unit}"
    
    def update_value(self, new_value, verbose=True):
        super().update_value(new_value)
        if verbose:
            print(f"Temperature updated to {self.value} {self.unit} in {self.room}")


class MotionSensor(Sensor):
    def __init__(self, name, room, value=False):
        super().__init__(name, room, value)
        self.last_motion_time = time.time()

    def read_value(self):
        status = "Motion Detected" if self.value else "No Motion"
        return f"{self.room}: {status}"
    
    def update_value(self, new_value, verbose=True):
        super().update_value(new_value)

        if new_value == True:
            self.last_motion_time = time.time()
            
        if verbose:
            status = "detected" if self.value else "not detected"
            print(f"Motion is now {status} in {self.room}")


class LightSensor(Sensor):
    def __init__(self, name, room, min_value=0, max_value=100):
        super().__init__(name, room)
        self.min_value = min_value
        self.max_value = max_value
        self.value = random.randint(self.min_value, self.max_value)

    def read_value(self):
        return f"Light in {self.room}: {self.value} % brightness"
    
    def update_value(self, new_value, verbose=True):
        if self.min_value <= new_value <= self.max_value:
            super().update_value(new_value)
            if verbose:
                print(f"Brightness updated to {self.value} % in {self.room}")
        else:
            print(f"Error: Brightness value {new_value} out of range ({self.min_value}-{self.max_value})")


class DoorSensor(Sensor):
    def __init__(self, name, room, value=False):
        super().__init__(name, room, value)

    def read_value(self):
        status = "Open" if self.value else "Closed"
        return f"Door in {self.room}: {status}"
    
    def update_value(self, new_value, verbose=True):
        super().update_value(new_value)
        if verbose:
            status = "open" if self.value else "closed"
            print(f"The door is now {status} in {self.room}")


class HumiditySensor(Sensor):
    def __init__(self, name, room, min_humidity=20, max_humidity=70):
        super().__init__(name, room)
        self.min_humidity = min_humidity
        self.max_humidity = max_humidity
        self.value = random.randint(self.min_humidity, self.max_humidity)

    def read_value(self):
        return f"Humidity in {self.room}: {self.value} % "  
    
    def update_value(self, new_value, verbose=True):
        if self.min_humidity <= new_value <= self.max_humidity:
            super().update_value(new_value)
            if verbose:
                print(f"Humidity updated to {self.value} % in {self.room}")
        else:
            print(f"Error: Humidity value {new_value} out of range ({self.min_humidity}-{self.max_humidity})")  

    
class SoilMoistureSensor(Sensor):
    def __init__(self, name, room, min_moisture=0, max_moisture=100):
        super().__init__(name, room)
        self.min_moisture = min_moisture
        self.max_moisture = max_moisture
        self.value = random.randint(self.min_moisture, self.max_moisture)

    def read_value(self):
        return f"Soil moisture in {self.room}: {self.value} % soil moisture"  
    
    def update_value(self, new_value, verbose=True):
        if self.min_moisture <= new_value <= self.max_moisture:
            super().update_value(new_value)
            if verbose:
                print(f"Soil moisture updated to {self.value} % in {self.room}")
        else:
            print(f"Error: Soil moisture value {new_value} out of range ({self.min_moisture}-{self.max_moisture})") 


class FloorCleanSensor(Sensor):
    def __init__(self, name, room, value=False):
        super().__init__(name, room, value)

    def read_value(self):
        status = "Clean" if self.value else "Dirty"
        return f"The floor in {self.room}: {status}" 
    
    def update_value(self, new_value, verbose=True):
        super().update_value(new_value)
        if verbose:
            status = "clean" if self.value else "dirty"
            print(f"The floor is now {status} in {self.room}")  
       

class DirtSensor(Sensor):
    def __init__(self, name, room, min_dirt=0, max_dirt=100):
        super().__init__(name, room)
        self.min_dirt = min_dirt
        self.max_dirt = max_dirt
        self.value = random.randint(self.min_dirt, self.max_dirt)

    def read_value(self):
        return f"Dirt level in {self.room}: {self.value} % dirt level"
    
    def update_value(self, new_value,verbose=True):
        if self.min_dirt <= new_value <= self.max_dirt:
            super().update_value(new_value)
            if verbose:
                print(f"Dirt level updated to {self.value} % in {self.room}")
        else:
            print(f"Error: Dirt level value {new_value} out of range ({self.min_dirt}-{self.max_dirt})")