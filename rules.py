import time
from datetime import datetime
from devices import SmartHeater, SmartAC, SmartLight, SmartSprinkler, SmartDishwasher, SmartDoorLock, SmartVacuumCleaner
from sensors import TemperatureSensor, MotionSensor, LightSensor, SoilMoistureSensor, DirtSensor, FloorCleanSensor


TEMP_LOW = 20
TEMP_HIGH = 25
LIGHT_THRESHOLD = 30
MOTION_TIMEOUT = 10 * 60


class AutomationRules:
    def __init__(self, devices_list, sensors_list):
        self.devices = devices_list
        self.sensors = sensors_list
        self.device_map = {d.name: d for d in devices_list}
        self.sensor_map = {s.name: s for s in sensors_list}


    def _find_device_in_same_room(self, target_room, device_class):
        for d in self.devices:
            if d.room == target_room and isinstance(d, device_class):
                return d
        return None


    def _find_sensor_in_same_room(self, target_room, sensor_class):
        for s in self.sensors:
            if s.room == target_room and isinstance(s, sensor_class):
                return s
        return None 
       


    #tempurature automation

    def apply_temperature_rules(self):
        for sensor in self.sensors:

            if not isinstance(sensor, TemperatureSensor):
                continue
            
            room = sensor.room
            temp = sensor.value

            heater = self._find_device_in_same_room(room, SmartHeater)
            ac = self._find_device_in_same_room(room, SmartAC)

            
            if heater and temp < TEMP_LOW:
                heater.turn_on()
                print(f"Temperature in {room} is {temp}°C. Turning on heater.")
                if ac:
                    ac.turn_off()
                continue

            
            if ac and temp > TEMP_HIGH:
                ac.turn_on()
                print(f"Temperature in {room} is {temp}°C. Turning on AC.")
                if heater:
                    heater.turn_off()
                continue

            
            if heater and heater.status == "ON" :
                heater.turn_off()
                print(f"Temperature in {room} is Comfortable. Turning off heater.")

            if ac and ac.status == "ON":
                ac.turn_off()
                print(f"Temperature in {room} is Comfortable. Turning off AC.") 


    #light automation

    def apply_light_rules(self):
        for sensor in self.sensors:

            if not isinstance(sensor, MotionSensor):
                continue
            
            room = sensor.room
            light = self._find_device_in_same_room(room, SmartLight)
            light_sensor = self._find_sensor_in_same_room(room, LightSensor)

            if not light or not light_sensor:
                continue

            if not hasattr(sensor, "last_motion_time"):
                continue

            seconds_since_motion = time.time() - sensor.last_motion_time
            
            is_dark = True

            if light_sensor and light_sensor.value >= LIGHT_THRESHOLD:
                is_dark = False

            if sensor.value and is_dark:
                if light.status == "OFF":
                    light.turn_on()
                    print(f"Motion detected in dark {room}. Turning on light.")
                    light.turn_on()

                    if hasattr(light, "set_brightness"):
                        light.set_brightness(80)

                elif not sensor.value and seconds_since_motion > MOTION_TIMEOUT:
                    if light.status == "ON":
                        print(f"No motion in {room} for {MOTION_TIMEOUT/60} minutes. Turning off light.")
                        light.turn_off()     
                    



    # security automation

    def apply_security_rules(self):
        door = self.sensor_map.get("Main Door Sensor")
        camera = self.device_map.get("Security Camera")
        door_lock = self.device_map.get("Main Door Lock")



        if not door or not camera:
            return
    
        is_recording = getattr(camera, "recording", False)

        if door.value and not is_recording:
            camera.start_recording()
            print("Main door opened. Starting security camera recording.")

        elif not door.value and is_recording:
            camera.stop_recording()
            print("Main door closed. Stopping security camera recording.")


        if door_lock:
            current_hour= datetime.now().hour
            AUTO_LOCK_HOUR = 22

            if current_hour >= AUTO_LOCK_HOUR and not door_lock.locked:
                door_lock.lock()
                print("It's late. Auto-locking the main door.")


    # garden automation

    def apply_garden_rules(self):
        for sensor in self.sensors:

            if not isinstance(sensor, SoilMoistureSensor):
                continue
            
            room = sensor.room
            sprinkler = self._find_device_in_same_room(room, SmartSprinkler)

            if not sprinkler:
                continue

            if sensor.value < 30 and sprinkler.status == "OFF":
                sprinkler.turn_on()
                print(f"Soil moisture in {room} is low ({sensor.value}%). Starting sprinkler.")

            elif sensor.value >= 80 and sprinkler.status == "ON":
                sprinkler.turn_off()
                print(f"Soil moisture in {room} is sufficient ({sensor.value}%). Stopping sprinkler.")  
    

    # dishwasher automation

    def apply_dishwasher_rules(self):
        for sensor in self.sensors:

            if not isinstance(sensor, DirtSensor):
                continue
            
            room = sensor.room
            dirt_level = sensor.value

            dishwasher = self._find_device_in_same_room(room, SmartDishwasher)

            if not dishwasher:
                continue

            if dirt_level > 70 and dishwasher.status == "OFF":
                dishwasher.turn_on()
                print(f"Dirt level in {room} is high . Starting dishwasher.")

            elif dirt_level <= 30 and dishwasher.status == "ON":
                dishwasher.turn_off()
                print(f"Dirt level in {room} is low . Stopping dishwasher.")
        


    # vacuum cleaner automation

    def apply_vacuum_rules(self):
        for sensor in self.sensors:

            if not isinstance(sensor, FloorCleanSensor):
                continue
            
            room = sensor.room
            is_clean = sensor.value

            vacuum = self._find_device_in_same_room(room, SmartVacuumCleaner)

            if not vacuum:
                continue

            if not is_clean and vacuum.status == "OFF":
                vacuum.turn_on()
                print(f"Floor in {room} is dirty. Starting vacuum cleaner.")

            elif is_clean and vacuum.status == "ON":
                vacuum.turn_off()
                print(f"Floor in {room} is clean. Stopping vacuum cleaner.")   




    def apply_all_checks(self):
        self.apply_temperature_rules()
        self.apply_light_rules()
        self.apply_security_rules()
        self.apply_garden_rules()
        self.apply_dishwasher_rules()
        self.apply_vacuum_rules()