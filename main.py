import customtkinter as ctk
from tkinter import messagebox
import time
from devices import *
from sensors import *
from controller import SmartHomeController

# -----theme-----
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("dark-blue")

class SmartHomeApp(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("🏠 Smart Home Ultimate OS")
        self.geometry("1280x850")
        
        self.status_indicators = {} 
        self.music_widgets = {} 

        
        self.device_classes = {
            "Air Conditioner": SmartAC, "Smart Light": SmartLight, "Smart TV": SmartTV,
            "Heater": SmartHeater, "Fan": SmartFan, "Door Lock": SmartDoorLock,
            "Camera": SmartCamera, "Sprinkler": SmartSprinkler, "Dishwasher": SmartDishwasher,
            "Coffee Maker": SmartCoffeeMaker, "Vacuum Cleaner": SmartVacuumCleaner,
            "Music System": SmartMusicSystem, "Smart Blinds": SmartBlinds
        }
        self.sensor_classes = {
            "Temperature Sensor": TemperatureSensor, "Motion Sensor": MotionSensor,
            "Light Sensor": LightSensor, "Door Sensor": DoorSensor,
            "Soil Moisture": SoilMoistureSensor, "Dirt Sensor": DirtSensor,
            "Floor Clean Sensor": FloorCleanSensor, "Humidity Sensor": HumiditySensor
        }

        self.show_login_screen()

    # --------login screen--------
    def show_login_screen(self):
        self.login_bg = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.login_bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        card = ctk.CTkFrame(self.login_bg, fg_color="#2b2b2b", corner_radius=20, 
                            border_width=2, border_color="#3a3a3a", width=400, height=350)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="🔒 ACCESS SYSTEM", font=("Impact", 24), text_color="#5dade2").pack(pady=(40, 20))
        
        self.pin_entry = ctk.CTkEntry(card, show="•", width=220, height=50, font=("Arial", 24), justify="center", corner_radius=10)
        self.pin_entry.pack(pady=10)
        self.pin_entry.focus()

        ctk.CTkButton(card, text="UNLOCK ", command=self.verify_login, width=220, height=50, 
                      font=("Arial", 14, "bold"), fg_color="#27ae60", hover_color="#2ecc71", corner_radius=10).pack(pady=20)
        
        self.bind('<Return>', lambda event: self.verify_login())

    def verify_login(self):
        if self.controller.check_pin(self.pin_entry.get()):
            self.login_bg.destroy()
            self.unbind('<Return>')
            self.build_main_interface()
        else:
            self.pin_entry.configure(border_color="red")
            self.pin_entry.delete(0, 'end')



    # ----------main interface----------    

    def build_main_interface(self):
        
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#212121")
        self.sidebar.pack(side="left", fill="y")
        
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(40, 40))
        ctk.CTkLabel(logo_frame, text="⚡ Homi", font=("Futura", 32, "bold"), text_color="#5dade2").pack()
        ctk.CTkLabel(logo_frame, text="SMART HOME OS", font=("Arial", 12), text_color="gray").pack()

        self.create_nav_btn("📊  Dashboard", self.show_dashboard)
        self.create_nav_btn("🌡️  Simulate Sensors", self.show_simulation)
        self.create_nav_btn("⚙️  System Modes", self.show_modes)
        self.create_nav_btn("🔋  Energy Monitor", self.show_energy)
        self.create_nav_btn("➕  Add Component", self.show_add_page)
        self.create_nav_btn("🛡️  Settings", self.show_settings)
        
        ctk.CTkButton(self.sidebar, text="⏻ Log Out", command=self.quit, fg_color="#c0392b", hover_color="#e74c3c", height=40).pack(side="bottom", fill="x", padx=20, pady=30)

        self.content_area = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a")
        self.content_area.pack(side="right", fill="both", expand=True)

        self.show_dashboard()

    def create_nav_btn(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, command=command, 
                            fg_color="transparent", text_color="#dce4e7", hover_color="#37474f",
                            anchor="w", font=("Arial", 15, "bold"), height=55, corner_radius=10)
        btn.pack(fill="x", padx=15, pady=5)

    def clear_content(self):
        for widget in self.content_area.winfo_children(): widget.destroy()

    def add_header(self, title, subtitle):
        f = ctk.CTkFrame(self.content_area, fg_color="transparent")
        f.pack(fill="x", padx=30, pady=(30, 20))
        ctk.CTkLabel(f, text=title, font=("Roboto", 32, "bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(f, text=subtitle, font=("Arial", 14), text_color="#a0a0a0").pack(anchor="w")



    # --------- dashboard page ---------

    def show_dashboard(self):
        self.clear_content()
        self.add_header("Dashboard", "Real-time device control")

        scroll = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        self.status_indicators = {}
        self.music_widgets = {} 

        row, col = 0, 0
        for device in self.controller.devices:
            if isinstance(device, SmartMusicSystem):
                if col == 1: 
                    row += 1
                    col = 0
                self.create_music_card(scroll, device, row, col)
                row += 1
                col = 0
            else:
                self.create_generic_card(scroll, device, row, col)
                col += 1
                if col > 1:
                    col = 0
                    row += 1

    def create_generic_card(self, parent, device, r, c):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color="#2b2b2b", border_width=1, border_color="#3a3a3a")
        card.grid(row=r, column=c, padx=10, pady=10, sticky="ew")
        
        status_color = self.get_status_color(device)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=12)
        
        icon = self.get_icon(device)
        ctk.CTkLabel(header, text=f"{icon}  {device.name}", font=("Arial", 16, "bold"), text_color="white").pack(side="left")
        
        indicator = ctk.CTkLabel(header, text="●", text_color=status_color, font=("Arial", 20))
        indicator.pack(side="right")
        self.status_indicators[device.name] = indicator

        ctk.CTkLabel(card, text=f"📍 {device.room}", font=("Arial", 12), text_color="gray").pack(anchor="w", padx=15, pady=(0, 10))

        controls = ctk.CTkFrame(card, fg_color="#212121", corner_radius=10)
        controls.pack(fill="x", padx=15, pady=(0, 15))

        is_on = (device.status == "ON")
        if isinstance(device, SmartDoorLock): is_on = device.locked

        switch_var = ctk.StringVar(value="on" if is_on else "off")
        switch_txt = "Lock" if isinstance(device, SmartDoorLock) else "Power"
        
        ctk.CTkSwitch(controls, text=switch_txt, variable=switch_var, onvalue="on", offvalue="off",
                      command=lambda: self.handle_toggle_no_reload(device, switch_var), 
                      font=("Arial", 13, "bold")).pack(side="right", padx=10, pady=10)

        if hasattr(device, 'set_brightness'):
            self.add_slider(controls, device, "Bright", 0, 100, device.brightness, device.set_brightness)
        elif hasattr(device, 'set_temperature'):
            self.add_slider(controls, device, "Temp", 16, 30, device.temperature, device.set_temperature)
        elif isinstance(device, SmartBlinds):
             self.add_slider(controls, device, "Open", 0, 100, device.position, device.set_position)

    def handle_toggle_no_reload(self, device, var):
        if isinstance(device, SmartDoorLock):
            if var.get() == "on": device.lock()
            else: device.unlock()
        else:
            if var.get() == "on": device.turn_on()
            else: device.turn_off()
        
        if device.name in self.status_indicators:
            new_color = self.get_status_color(device)
            self.status_indicators[device.name].configure(text_color=new_color)

    def get_status_color(self, device):
        if isinstance(device, SmartDoorLock):
            return "#00e676" if device.locked else "#ff5252"
        return "#00e676" if device.status == "ON" else "#ff5252"

    def get_icon(self, device):
        if isinstance(device, SmartLight): return "💡"
        if isinstance(device, SmartAC): return "❄️"
        if isinstance(device, SmartHeater): return "🔥"
        if isinstance(device, SmartTV): return "📺"
        if isinstance(device, SmartCamera): return "📷"
        if isinstance(device, SmartDoorLock): return "🔒"
        if isinstance(device, SmartBlinds): return "🪟"
        return "🔌"

    

    #--------- music card ---------

    def create_music_card(self, parent, device, r, c):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color="#1e1e2e", border_width=2, border_color="#8e44ad")
        card.grid(row=r, column=c, columnspan=2, padx=10, pady=10, sticky="ew")
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(header, text="🎵  Media Center", font=("Arial", 16, "bold"), text_color="#bb86fc").pack(side="left")
        ctk.CTkLabel(header, text=f"{device.name}", text_color="gray").pack(side="right")

        screen = ctk.CTkFrame(card, fg_color="black", corner_radius=10, height=40)
        screen.pack(fill="x", padx=20, pady=5)
        
        song_txt = f"🎶 {device.current_song}" if device.status == "ON" and device.current_song else "⏹ Stopped"
        song_label = ctk.CTkLabel(screen, text=song_txt, font=("Consolas", 14), text_color="#03dac6")
        song_label.pack(pady=10)

        ctrl = ctk.CTkFrame(card, fg_color="transparent")
        ctrl.pack(fill="x", padx=20, pady=10)
        self.add_slider(ctrl, device, "Vol", 0, 100, device.volume, device.set_volume)

        vals = device.playlist if device.playlist else ["(Empty)"]
        music_menu = ctk.CTkOptionMenu(ctrl, values=vals, width=150, dynamic_resizing=False,
                                            command=lambda s: self.play_specific_song_smooth(device, s))
        music_menu.set("Playlist")
        music_menu.pack(side="right", padx=10)

        ctk.CTkButton(ctrl, text="🗑️", width=30, fg_color="#c0392b", command=lambda: self.remove_song_gui(device, music_menu)).pack(side="right", padx=2)
        ctk.CTkButton(ctrl, text="➕", width=30, fg_color="#27ae60", command=lambda: self.add_song_gui(device, music_menu)).pack(side="right", padx=2)

        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.pack(pady=(0, 15))
        
        ctk.CTkButton(btns, text="⏮", width=50, fg_color="#333", 
                      command=lambda: [device.previous_song(), self.update_music_ui(device)]).pack(side="left", padx=5)
        
        play_txt = "⏹ Stop" if device.status == "ON" else "▶ Play"
        play_col = "#c0392b" if device.status == "ON" else "#27ae60"
  
        play_btn = ctk.CTkButton(btns, text=play_txt, width=80, fg_color=play_col, 
                      command=lambda: self.handle_music_toggle_smooth(device))
        play_btn.pack(side="left", padx=5)
        
        ctk.CTkButton(btns, text="⏭", width=50, fg_color="#333", 
                      command=lambda: [device.next_song(), self.update_music_ui(device)]).pack(side="left", padx=5)

        self.music_widgets[device.name] = {
            "label": song_label,
            "play_btn": play_btn,
            "menu": music_menu
        }

    def update_music_ui(self, device):
        """تحديث شكل كارت الموسيقى فقط"""
        widgets = self.music_widgets.get(device.name)
        if not widgets: return

        new_txt = f"🎶 {device.current_song}" if device.status == "ON" and device.current_song else "⏹ Stopped"
        widgets["label"].configure(text=new_txt)

        new_play_txt = "⏹ Stop" if device.status == "ON" else "▶ Play"
        new_play_col = "#c0392b" if device.status == "ON" else "#27ae60"
        widgets["play_btn"].configure(text=new_play_txt, fg_color=new_play_col)

        new_vals = device.playlist if device.playlist else ["(Empty)"]
        widgets["menu"].configure(values=new_vals)

    def handle_music_toggle_smooth(self, device):
        if device.status == "ON": device.turn_off()
        else: device.turn_on()
        self.update_music_ui(device) 

    def play_specific_song_smooth(self, device, song):
        if song in device.playlist:
            device.current_song = song
            if device.status == "OFF": device.turn_on()
            self.update_music_ui(device)

    def add_song_gui(self, device, menu_widget):
        dialog = ctk.CTkInputDialog(text="Enter Song Name:", title="Add to Playlist")
        song = dialog.get_input()
        if song:
            device.add_song(song)
            self.update_music_ui(device)

    def remove_song_gui(self, device, menu_widget):
        selected = menu_widget.get()
        if selected in device.playlist:
            device.remove_song(selected)
            self.update_music_ui(device)
            menu_widget.set("Playlist") 
        else:
            messagebox.showwarning("Error", "Select a song from the dropdown first.")

    def add_slider(self, parent, device, label, min_v, max_v, current, setter):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(side="left", padx=5)
        ctk.CTkLabel(f, text=label, font=("Arial", 10)).pack(side="left", padx=2)
        s = ctk.CTkSlider(f, from_=min_v, to=max_v, number_of_steps=(max_v-min_v), width=100, progress_color="#5dade2")
        s.set(current)
        s.pack(side="left")
        s.bind("<ButtonRelease-1>", lambda e: setter(int(s.get())))



    #-------- sensor simulation page ---------
 
    def show_simulation(self):
        self.clear_content()
        self.add_header("Sensor Simulator", "Manually change environment values")
        scroll = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20)
        for sensor in self.controller.sensors:
            card = ctk.CTkFrame(scroll, fg_color="#2b2b2b")
            card.pack(fill="x", pady=5)
            ctk.CTkLabel(card, text=f"📡 {sensor.name}", font=("Arial", 14, "bold"), width=200, anchor="w").pack(side="left", padx=20)
            
            input_frame = ctk.CTkFrame(card, fg_color="transparent")
            input_frame.pack(side="right", padx=20)

            if isinstance(sensor, (MotionSensor, DoorSensor, FloorCleanSensor)):
                seg = ctk.CTkSegmentedButton(input_frame, values=["Inactive", "Active"], 
                                             command=lambda v, s=sensor: self.update_bool_sensor(s, v))
                seg.set("Active" if sensor.value else "Inactive")
                seg.pack()
            elif isinstance(sensor, TemperatureSensor):
                lbl = ctk.CTkLabel(input_frame, text=f"{sensor.value}°C", width=50); lbl.pack(side="left")
                slider = ctk.CTkSlider(input_frame, from_=0, to=50, width=150)
                slider.set(sensor.value); slider.pack(side="left")
                slider.bind("<ButtonRelease-1>", lambda e, s=sensor, l=lbl, sl=slider: self.update_num_sensor(s, sl.get(), l, "°C"))
            else:
                lbl = ctk.CTkLabel(input_frame, text=f"{sensor.value}%", width=50); lbl.pack(side="left")
                slider = ctk.CTkSlider(input_frame, from_=0, to=100, width=150)
                slider.set(sensor.value); slider.pack(side="left")
                slider.bind("<ButtonRelease-1>", lambda e, s=sensor, l=lbl, sl=slider: self.update_num_sensor(s, sl.get(), l, "%"))

    def update_bool_sensor(self, sensor, value_str):
        new_val = True if value_str == "Active" else False
        sensor.update_value(new_val)
        
        self.trigger_automation_check()

    def update_num_sensor(self, sensor, val, label_widget, unit):
        new_val = int(val)
        sensor.update_value(new_val)
        label_widget.configure(text=f"{new_val}{unit}")
        
        self.trigger_automation_check()

    def trigger_automation_check(self):
        if self.controller.system_mode != "Auto":
            print(f"⚠️ Rules Skipped: System is in '{self.controller.system_mode}' mode.")
            return

        print("🔄 Sensor changed -> Running Rules...")
        self.controller.apply_automation_rules()



    # -------------modes page -------------

    def show_modes(self):
        self.clear_content()
        self.add_header("System Modes", "Select Home Scenario")
        grid = ctk.CTkFrame(self.content_area, fg_color="transparent")
        grid.pack(fill="x", expand=False, padx=40, pady=40)
        grid.grid_columnconfigure((0, 1, 2), weight=1)
        self.create_big_mode_btn(grid, 0, "🤖 AUTO", "AI Control", "#4bb577", "Auto")
        self.create_big_mode_btn(grid, 1, "💤 SLEEP", "Lights OFF", "#377ca9", "Sleep")
        self.create_big_mode_btn(grid, 2, "👋 AWAY", "Secure Mode", "#884fd3", "Away")

    def create_big_mode_btn(self, parent, col, title, sub, color, mode_name):
        border_col = "white" if self.controller.system_mode == mode_name else color
        border_w = 4 if self.controller.system_mode == mode_name else 0
        btn = ctk.CTkButton(parent, text=f"{title}\n\n{sub}", font=("Arial", 24, "bold"), fg_color=color, hover_color=color,
                            corner_radius=20, border_color=border_col, border_width=border_w,height=400,
                            command=lambda: self.activate_mode(mode_name))
        btn.grid(row=0, column=col, padx=10, sticky="ew")

    def activate_mode(self, mode):
        self.controller.set_system_mode(mode)
        messagebox.showinfo("Mode Activated", f"System switched to {mode} Mode!")
        self.show_modes()


    # --------- energy reporter page ---------
   
    def show_energy(self):
        self.clear_content()
        self.add_header("Energy Monitor", "Usage Stats")
        data, total = self.controller.get_energy_report()
        sum_card = ctk.CTkFrame(self.content_area, fg_color="#20847f", height=80)
        sum_card.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(sum_card, text=f"Total: {total} kWh", font=("Arial", 28, "bold"), text_color="white").pack(side="left", padx=30)
        tbl = ctk.CTkScrollableFrame(self.content_area); tbl.pack(fill="both", expand=True, padx=20)
        for item in data:
            r = ctk.CTkFrame(tbl, fg_color="#2b2b2b"); r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=f"{item['name']}", width=200, anchor="w").pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(r, text=f"{item['kwh']} kWh", text_color="#2DD0E9").pack(side="right", padx=20)



    #----------- add device/sensor page ---------

    def show_add_page(self):
        self.clear_content()
        self.add_header("Add Component", "Expand System")
        p = ctk.CTkFrame(self.content_area, fg_color="#2b2b2b"); p.pack(pady=20, padx=20, fill="both")
        self.cat_var = ctk.StringVar(value="Device")
        ctk.CTkSegmentedButton(p, values=["Device", "Sensor"], variable=self.cat_var, command=self.update_type).pack(pady=20)
        self.type_menu = ctk.CTkOptionMenu(p, width=300); self.type_menu.pack(pady=10)
        self.update_type("Device")
        self.name_ent = ctk.CTkEntry(p, width=300, placeholder_text="Name"); self.name_ent.pack(pady=10)
        self.room_ent = ctk.CTkEntry(p, width=300, placeholder_text="Room"); self.room_ent.pack(pady=10)
        ctk.CTkButton(p, text="Add", command=self.save_item, fg_color="#00e676", text_color="black").pack(pady=30)

    def update_type(self, choice):
        vals = list(self.device_classes.keys()) if choice == "Device" else list(self.sensor_classes.keys())
        self.type_menu.configure(values=vals); self.type_menu.set(vals[0])

    def save_item(self):
        cat, typ, nm, rm = self.cat_var.get(), self.type_menu.get(), self.name_ent.get(), self.room_ent.get()
        if not nm or not rm: return messagebox.showerror("Error", "Required")
        try:
            cls = self.device_classes[typ] if cat == "Device" else self.sensor_classes[typ]
            obj = cls(name=nm, room=rm)
            if cat == "Device": self.controller.add_device(obj)
            else: self.controller.add_sensor(obj)
            messagebox.showinfo("Success", "Added"); self.name_ent.delete(0,'end'); self.room_ent.delete(0,'end')
        except Exception as e: messagebox.showerror("Error", str(e))


    # -------settings page ---------
   
    def show_settings(self):
        self.clear_content()
        self.add_header("Security Settings", "Manage Access PIN")

        panel = ctk.CTkFrame(self.content_area, fg_color="#2b2b2b", corner_radius=15)
        panel.pack(pady=40, padx=40, fill="both")

        ctk.CTkLabel(panel, text="Change Security PIN", font=("Arial", 18, "bold")).pack(pady=(30, 20))

        ctk.CTkLabel(panel, text="Current PIN:").pack(pady=5)
        old_entry = ctk.CTkEntry(panel, show="*", width=250)
        old_entry.pack(pady=5)

        ctk.CTkLabel(panel, text="New PIN:").pack(pady=5)
        new_entry = ctk.CTkEntry(panel, show="*", width=250)
        new_entry.pack(pady=5)

        def update_pin():
            success, msg = self.controller.change_pin(old_entry.get(), new_entry.get())
            if success:
                messagebox.showinfo("Success", msg)
                old_entry.delete(0, 'end'); new_entry.delete(0, 'end')
            else:
                messagebox.showerror("Error", msg)

        ctk.CTkButton(panel, text="Update Password", command=update_pin, fg_color="#e67e22", width=250, height=40).pack(pady=30)



if __name__ == "__main__":
    c = SmartHomeController()
    
    # Music
    m = SmartMusicSystem("Living Room Audio", "Living Room")
    m.add_song("Morning Jazz"); m.add_song("LoFi Beats"); m.add_song("Classical")
    c.add_device(m)
    
    # Living Room
    c.add_device(SmartAC("Main AC", "Living Room"))
    c.add_device(SmartLight("Ceiling Light", "Living Room"))
    c.add_device(SmartBlinds("Main Window", "Living Room"))
    c.add_device(SmartTV("Samsung TV", "Living Room"))
    
    # Bedroom
    c.add_device(SmartAC("Air conditioner", "Bedroom"))
    c.add_device(SmartLight("Night Lamp", "Bedroom"))
    c.add_device(SmartFan("Ceiling Fan", "Bedroom"))
    c.add_device(SmartHeater("Heater", "Bedroom"))

    # Kitchen
    c.add_device(SmartLight("Kitchen Light", "Kitchen"))
    c.add_device(SmartDishwasher("Dishwasher", "Kitchen"))
    c.add_device(SmartCoffeeMaker("Coffee Machine", "Kitchen"))

    # Security
    c.add_device(SmartDoorLock("Front Door Lock", "Entrance"))
    c.add_device(SmartCamera("Door Cam", "Entrance"))

    # Garden
    c.add_device(SmartSprinkler("Lawn Sprinkler", "Backyard"))
    c.add_device(SmartCamera("Backyard Cam", "Main Garden"))

    # Sensors
    c.add_sensor(TemperatureSensor("LR Thermostat", "Living Room", 22))
    c.add_sensor(MotionSensor("LR Motion", "Living Room", True))
    c.add_sensor(DoorSensor("Main Door Sensor", "Entrance", False))
    c.add_sensor(SoilMoistureSensor("Soil Sensor", "Backyard", 40))

    app = SmartHomeApp(c)
    app.mainloop()