# Project: 2D ScanEngine
### A 2D Scan Controller Framework for Simulated Stage and Sensor Systems
---
This project implements a **2D Scan Controller** for simulated hardware components that maybe used in any industry.  
The controller automates moving a stage in a 2D grid, collects sensor measurements, and provides visualization.

## ⚙️ Features

- ✅Configurable 2D grid scan (X and Y ranges, step size)
- ✅Stage movement with retry mechanism
- ✅Sensor data collection with rolling-average filtering
- ✅Peak detection and result saving
- ✅CSV output of raw, filtered, and peak data
- ✅Heatmap visualization of scan results

## 🗂️ project Structure
#### QD_Task/
- **requirements.txt** - Required Python packages 
- config.yaml : Scan configuration file
- Jupyter_demo.ipynb : Jupyter Notebook demo (visualization)
- unit_tests.py : Unit tests for key functions
- config.py : YAML config parser utility
- functions.py : Move stage + measure sensor with retries
- scan_controller.py : Main scan controller CLI
- Visualize.py : Heatmap plotting utilities
- sim_devices.py : Simulated hardware devices (SimStage, SimSensor)
#### QD_Task/output/
- scan_data.csv : Output CSV (created after scan)
- heatmap.png : Output heatmap image (created after visualization)
- scan.log : Log of the last scan run 

...

---

## 🚀 Setup & Usage

### 1️⃣ Install dependencies

1. Clone the repository.
2. (Optional) Create and activate a virtual environment.
3. Install required packages using the provided `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

### 2️⃣ Usage

1. Configure scan parameters in `config.yaml` (X/Y range, retries, filter and logging settings).
2. Run the 2D scan and save results:
    ```bash
    python scan_controller.py
    ```
3. Generate heatmap visualization:
    ```bash
    python visualize.py
    ```
4. Test the system:
    ```bash
    python -m  unittest discover -p "*_Tests.py" -v   
    ```
### 3️⃣ Results
After running the scan and visualization, the following files are saved in the `output/` folder:

- `scan_data.csv` — Contains x,y points, raw sensor values, filtered values, and peak detection details at the end of the file.
- `heatmap.png` — Heatmap visualization of filtered sensor values.
- `scan.log` — Log file with scan execution details.
