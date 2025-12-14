# 🏠 Homi — Smart Home Ultimate OS

**Homi** is a fully modular, Python-based Smart Home Operating System designed to simulate real-world smart home behavior using Object-Oriented Programming principles.  
The system focuses on scalability, automation intelligence, and clean architecture rather than simple device control.

This project demonstrates strong software engineering practices including modular design, separation of concerns, and rule-based automation.

---

## 🌟 Why Homi?
Unlike basic smart home simulations, **Homi** is designed as a centralized operating system that:
- Manages devices and sensors as independent entities
- Applies intelligent automation rules
- Supports system-wide modes and energy awareness
- Can scale easily with new devices, sensors, or automation logic

---

## 🚀 Core Features
- Centralized smart home management system
- Modular and extensible architecture
- Smart device control (Lights, AC, etc.)
- Environmental sensors (Temperature, Motion)
- Rule-based automation engine
- System modes (Sleep / Away)
- Energy usage monitoring and reporting
- Clean OOP-based code structure

---

## 🧠 System Architecture & Design
Homi follows a **layered modular architecture**, where each responsibility is isolated into its own component:

### Device Layer
- `devices.py`  
  Handles all controllable smart devices and tracks their power usage.

### Sensor Layer
- `sensors.py`  
  Reads and processes environmental data such as temperature and motion.

### Control Layer
- `controller.py`  
  Acts as the system’s core brain:
  - Manages devices and sensors
  - Controls system modes
  - Generates energy consumption reports

### Automation Layer
- `rules.py`  
  Implements rule-based automation logic that makes intelligent decisions based on sensor input.

### Application Entry Point
- `main.py`  
  Initializes the system and runs the smart home simulation.

---

## 🛠 Technologies & Concepts
- Python
- Object-Oriented Programming (OOP)
- Modular & Layered Architecture
- Rule-Based Automation
- Clean Code Principles

---

## ▶️ Running the Project
```bash
python main.py