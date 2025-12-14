import time

class Device:
    def __init__(self, name, room, power_usage, status='OFF'):
        self.name = name
        self.power_usage = power_usage
        self.room = room
        self.status = status
        self.start_time = None
        self.total_hours = 0

    def turn_on(self):
        if self.status == 'OFF':
            self.status = 'ON'
            self.start_time = time.time()
            print(f"{self.name} is now {self.status}.")

    def turn_off(self):
        if self.status == 'ON':
            self.status = 'OFF'
            end_time = time.time()
            hours_used = (end_time - self.start_time) / 3600
            self.total_hours += hours_used
            self.start_time = None
            print(f"{self.name} is now {self.status}. Total hours used: {self.total_hours:.2f} hours.")

    def get_status(self):
        return f"{self.name} is currently {self.status}."
    

class SmartLight(Device):
    def __init__(self, name, room, power_usage=5, brightness=50, color='White'):
        super().__init__(name, room, power_usage)
        self.brightness = brightness
        self.color = color

    def set_brightness(self, brightness):
        if 0 <= brightness <= 100:
            self.brightness = brightness
            print(f"{self.name} brightness set to {self.brightness}%.")

        else:
            print("Brightness must be between 0 and 100.")
        

    def set_color(self, color):
        self.color = color
        print(f"{self.name} color set to {self.color}.")

    def turn_on(self):
        super().turn_on()
        print(f"{self.name} is now {self.status} with brightness {self.brightness}% and color {self.color}.")   


    def turn_off(self):
        super().turn_off()


class SmartFan(Device):
    def __init__(self, name, room, power_usage=10, speed=1):
        super().__init__(name, room, power_usage)
        self.speed = speed

    def set_speed(self, speed):
        self.speed = speed
        print(f"{self.name} speed set to {self.speed}.")

    def turn_on(self):
        super().turn_on()
        print(f"{self.name} is now {self.status} at speed {self.speed}.")

    def turn_off(self):
        super().turn_off()


class SmartAC(Device):
    def __init__(self, name, room, power_usage=1500, temperature=24):
        super().__init__(name, room, power_usage)
        self.temperature = temperature

    def set_temperature(self, temperature):
        if temperature < 16 or temperature > 30:
            print("Temperature must be between 16°C and 30°C.") 

        else:
            self.temperature = temperature
            print(f"{self.name} temperature set to {self.temperature}°C.")  


    def turn_on(self):
        super().turn_on()
        print(f"{self.name} is now {self.status} at {self.temperature}°C.")

    def turn_off(self):
        super().turn_off()


class SmartHeater(Device):
    def __init__(self, name, room, power_usage=2000, temperature=22):
        super().__init__(name, room, power_usage)
        self.temperature = temperature

    def set_temperature(self, temperature):
        self.temperature = temperature
        print(f"{self.name} temperature set to {self.temperature}°C.")

    def turn_on(self):
        super().turn_on()
        print(f"{self.name} is now {self.status} at {self.temperature}°C.")

    def turn_off(self):
        super().turn_off()
        print(f"{self.name} is now {self.status}.")


class SmartDoorLock(Device):
    def __init__(self, name, room, power_usage=2, locked=True):
        super().__init__(name, room, power_usage)
        self.locked = locked

    def lock(self):
        self.locked = True
        print(f"{self.name} is now locked.")

    def unlock(self):
        self.locked = False
        print(f"{self.name} is now unlocked.")

    def get_status(self):
        return super().get_status() + f" It is currently {'locked' if self.locked else 'unlocked'}."
    

class SmartCamera(Device):
    def __init__(self, name, room, power_usage=8, recording=False):
        super().__init__(name, room, power_usage)
        self.recording = recording

    def start_recording(self):
        self.recording = True
        print(f"{self.name} has started recording.")

    def stop_recording(self):
        self.recording = False
        print(f"{self.name} has stopped recording.")

    def get_status(self):
        return super().get_status() + f" It is currently {'recording' if self.recording else 'not recording'}."
    

class SmartMusicSystem(Device):
    def __init__(self, name, room, power_usage=20, volume=50):
        super().__init__(name, room, power_usage)
        self.volume = volume
        self.playlist = []
        self.current_song = None


    def add_song(self, song):
        self.playlist.append(song)
        print(f"'{song}' added to {self.name} playlist.")

    def remove_song(self, song):
        if song in self.playlist:
            self.playlist.remove(song)
            print(f"'{song}' removed from {self.name} playlist.")
        else:
            print(f"'{song}' not found in {self.name} playlist.")

    def set_volume(self, volume):
        if 0 <= volume <= 100:
            self.volume = volume
            print(f"{self.name} volume set to {self.volume}%.")

        else:
            print("Volume must be between 0 and 100.")


    def show_playlist(self):
        if self.playlist:
            print(f"{self.name} Playlist:")
            for idx, song in enumerate(self.playlist,1):
                print(f"{idx}. {song}")
        else:
            print(f"{self.name} playlist is empty.")

    def turn_on(self):
        if self.playlist:
            self.status = 'ON'
            self.start_time = time.time()
            self.current_song = self.playlist[0]
            print(f"{self.name} is now {self.status}. Playing '{self.current_song}' at volume {self.volume}%.")
        else:
            print(f"{self.name} cannot be turned on. Playlist is empty.")

    def turn_off(self):
        super().turn_off()
        self.current_song = None
        print(f"{self.name} has stopped playing music.")

    def next_song(self):
        if self.playlist and self.current_song:
            current_index = self.playlist.index(self.current_song)
            next_index = (current_index + 1) % len(self.playlist)
            self.current_song = self.playlist[next_index]
            print(f"{self.name} is now playing '{self.current_song}'.")
        else:
            print(f"{self.name} cannot go to the next song. Playlist is empty or music is not playing.")

    def previous_song(self):
        if self.playlist and self.current_song:
            current_index = self.playlist.index(self.current_song)
            previous_index = (current_index - 1) % len(self.playlist)
            self.current_song = self.playlist[previous_index]
            print(f"{self.name} is now playing '{self.current_song}'.")
        else:
            print(f"{self.name} cannot go to the previous song. Playlist is empty or music is not playing.")

    def get_status(self):
        status = super().get_status()
        if self.current_song:
            status += f" Currently playing '{self.current_song}' at volume {self.volume}%."
        else:
            status += " No song is currently playing."
        return status


class SmartBlinds(Device):
    def __init__(self, name, room, power_usage=3, position=0):
        super().__init__(name, room, power_usage)
        self.position = position  # 0 = closed, 100 = fully open

    def set_position(self, position):
        self.position = position
        print(f"{self.name} position set to {self.position}% open.")

    def turn_on(self):
        super().turn_on()
        print(f"{self.name} blinds are now open at {self.position}%.")

    def turn_off(self):
        super().turn_off()
        self.position = 0
        print(f"{self.name} blinds are  now closed.")

    
class SmartSprinkler(Device):
    def __init__(self, name, room, power_usage=12, duration=10):
        super().__init__(name, room, power_usage)
        self.duration = duration  # in minutes

    def set_duration(self, duration):
        self.duration = duration
        print(f"{self.name} watering duration set to {self.duration} minutes.")

    def turn_on(self):
        super().turn_on()
        print(f"{self.name} is now watering for {self.duration} minutes.")

    def turn_off(self):
        super().turn_off()
        print(f"{self.name} has stopped watering.")

    
class SmartCoffeeMaker(Device):
    def __init__(self, name, room, power_usage=800, brew_strength='Medium'):
        super().__init__(name, room, power_usage)
        self.brew_strength = brew_strength

    def set_brew_strength(self, strength):
        self.brew_strength = strength
        print(f"{self.name} brew strength set to {self.brew_strength}.")

    def turn_on(self):
        super().turn_on()
        print(f"{self.name} is now brewing coffee with {self.brew_strength} strength.")

    def turn_off(self):
        super().turn_off()
        print(f"{self.name} has stopped brewing coffee.")


class SmartVacuumCleaner(Device):
    def __init__(self, name, room, power_usage=150, cleaning_mode='Auto'):
        super().__init__(name, room, power_usage)
        self.cleaning_mode = cleaning_mode

    def set_cleaning_mode(self, mode):
        self.cleaning_mode = mode
        print(f"{self.name} cleaning mode set to {self.cleaning_mode}.")

    def turn_on(self):
        super().turn_on()
        print(f"{self.name} is now cleaning in {self.cleaning_mode} mode.")

    def turn_off(self):
        super().turn_off()
        print(f"{self.name} has stopped cleaning.")


class SmartDishwasher(Device):
    def __init__(self, name, room, power_usage=1200, wash_cycle='Normal'):
        super().__init__(name, room, power_usage)
        self.wash_cycle = wash_cycle

    def set_wash_cycle(self, cycle):
        self.wash_cycle = cycle
        print(f"{self.name} wash cycle set to {self.wash_cycle}.")

    def turn_on(self):
        super().turn_on()
        print(f"{self.name} is now running the {self.wash_cycle} wash cycle.")

    def turn_off(self):
        super().turn_off()
        print(f"{self.name} has stopped the wash cycle.")


class SmartTV(Device):
    def __init__(self, name, room, power_usage=100, channel=1, volume=20):
        super().__init__(name, room, power_usage)
        self.channel = channel
        self.volume = volume

    def set_channel(self, channel):
        self.channel = channel
        print(f"{self.name} channel set to {self.channel}.")

    def set_volume(self, volume):
        self.volume = volume
        print(f"{self.name} volume set to {self.volume}%.")

    def turn_on(self):
        super().turn_on()
        print(f"{self.name} is now on channel {self.channel} at volume {self.volume}%.")

    def turn_off(self):
        super().turn_off()

    



