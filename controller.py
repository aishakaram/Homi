from rules import AutomationRules
from devices import *

class SmartHomeController:
    def __init__ (self):
        self.devices = []
        self.sensors = []
        self.automation_rules = None
        self.pin = "1234" #default pin
        self.system_mode ="Auto"

    
    #manage devices and sensors

    def add_device(self, device):
        self.devices.append(device)
        print(f"Device Added: {device.name} in {device.room}")

    
    def add_sensor(self, sensor):
        self.sensors.append(sensor)
        print(f"Sensor Added: {sensor.name} in {sensor.room}")


    #security methods

    def check_pin(self, input_pin):
        return input_pin == self.pin
    
    def change_pin(self, old_pin, new_pin):
        if self.check_pin(old_pin):
            self.pin = new_pin
            print("✅ PIN changed successfully.")
        else:
            print("❌ Incorrect old PIN. PIN change failed.")




    


    #syestem mode methods
    
    def set_system_mode(self, mode):
        self.system_mode = mode
        print(f"🔄 System Mode changed to: {mode}")
        
        if mode == "Sleep":
            print("💤 Executing Sleep Protocol...")
            for dev in self.devices:
              
                if isinstance(dev, SmartDoorLock):
                    dev.lock()
               
                if isinstance(dev, (SmartLight, SmartMusicSystem, SmartTV, SmartCoffeeMaker, SmartSprinkler)):
                    dev.turn_off()
                
                if isinstance(dev, SmartBlinds):
                    dev.turn_off() 

                if isinstance(dev, SmartCamera):
                    dev.turn_on()
                    dev.start_recording()

                    
        elif mode == "Away":
            print("👋 Executing Away Protocol...")
            for dev in self.devices:
                
                if isinstance(dev, SmartDoorLock):
                    dev.lock()
               
                if isinstance(dev, (SmartAC, SmartHeater, SmartCoffeeMaker, SmartTV, SmartMusicSystem)):
                    dev.turn_off()
                
                if isinstance(dev, SmartCamera):
                    dev.turn_on()
                    dev.start_recording()
                
                if isinstance(dev, SmartVacuumCleaner):
                    dev.turn_on()




    #energy reporting methods

    def get_energy_report(self):
        report_data = []
        total_kwh = 0.0

        for d in self.devices:
            hours = getattr(d,'total_hours',0)
            
            if hours ==0: hours = 1
            kwh = (d.power_usage * hours)/ 1000
            total_kwh += kwh

            report_data.append({
                "name": d.name, 
                "room": d.room,
                "hours": round(hours,2),
                "kwh": round(kwh,4)
            })

        return report_data, round(total_kwh,4)


    
    #operations methods

    def read_all_sensors(self):
        print("\n" + "="*50)
        print("\n--- 📡 SENSORS STATUS ---")
        sorted_sensors = sorted(self.sensors, key=lambda x: x.room)
        for s in sorted_sensors:
            print(f"📍 [{s.room}] {s.name} : {s.value}")
        print("-"*50)



    def apply_automation_rules(self):
        if self.system_mode != "Auto":
            print(f"⚠️ Automation skipped: System is in {self.system_mode} mode.")
            return
        
        self.automation_rules = AutomationRules(self.devices, self.sensors)
        print("🤖 Applying AI Automation Rules ....")
        self.automation_rules.apply_all_checks()




    def show_status(self):
        
        print("\n" + "="*50)
        print(f"{'🏠 SMART HOME DASHBOARD':^50}")
        print(f"System Mode: {self.system_mode:^50}")
        print("="*50)

        print("\n--- 🔌 DEVICES STATUS ---")
        sorted_devices = sorted(self.devices, key=lambda x: x.room)

        for d in sorted_devices:
            icon = "🟢" if d.status == "ON" else "🔴"
            if hasattr(d, 'locked'): icon = "🔒" if d.locked else "🔓"

            details = ""
            if hasattr(d, 'temperature'): details = f"Set: {d.temperature}°C"
            elif hasattr(d, 'brightness'): details = f"Bright: {d.brightness}%"

            print(f"{icon} [{d.room}] {d.name:<20} : {d.status}     {details}")     

        print("-"*50)



        print("\n--- 📡 SENSORS STATUS ---")
        sorted_sensors = sorted(self.sensors, key=lambda x: x.room)
        for s in sorted_sensors:
            print(f"📍 [{s.room}] {s.name} : {s.value}")
        print("-"*50)





    

