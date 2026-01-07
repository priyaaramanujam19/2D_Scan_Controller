import numpy as np
import logging
import csv
import matplotlib
import matplotlib.pyplot as plt
import os
from config import load_yaml_file
from functions import move_stage, measure_sensor, stage, sensor

config = load_yaml_file()
#this is a dummy comment

# Function to store x and y points in an array
def generate_scan_points(x_range, y_range):
    x_values = np.linspace(x_range["start"], x_range["end"], x_range["steps"], dtype = int)
    y_values = np.linspace(y_range["start"], y_range["end"], y_range["steps"], dtype = int)
    points = []
    for i, y in enumerate(y_values): #zig zag method scan 
        if i % 2 == 0:
            for x in x_values:   # Even row: left to right
                points.append((x, y))
        else:
            for x in reversed(x_values): # Odd row: right to left
                points.append((x, y))
    return points #returns x,y points

# Function to calculate rolling average
"""
Updates the list of recent values with the new_value, then
does rolling average based on the window size , and returns the current average.
"""
def compute_rolling_average(recent_values, new_value, window_size):
    recent_values.append(new_value)
    if len(recent_values) > window_size:
        recent_values.pop(0) #removes the first stored value
    return round(sum(recent_values) / len(recent_values), 2)


def detect_peak(results):
    valid_points = [row for row in results if row[3] is not None]
    if valid_points:
        peak_value = max(row[3] for row in valid_points)
        peak_point = max(valid_points, key=lambda row: row[3])
        return peak_value, (peak_point[0], peak_point[1])
    else:
        return None, None
    
    
# MAIN FUNCTION 
def perform_scan(config, return_peak=False): #return_peak is helper code to turn off logging peak values in csv
    scan_points = generate_scan_points(config["x_range"], config["y_range"])
    max_retries = config["max_retries"]
    window_size = config["rolling_window_size"]
    results = []  # to store (x, y, raw, filtered)
    recent_values = []  # for rolling average
    
    for (x, y) in scan_points:
        moved = move_stage(x, y, max_retries) #Start moving the stage
        if not moved:
            logging.warning(f"Skipping point ({x}, {y}) due to move failure.")
            results.append((x, y, None, None))
            continue

        raw = measure_sensor(x,y,max_retries) # Start sensor measurement
        if raw is None:
            logging.warning(f"Skipping point ({x}, {y}) due to measure failure.")
            results.append((x, y, None, None))
            continue

        #Call rolling average function
        filtered = compute_rolling_average(recent_values, raw, window_size)

        results.append((x, y, raw, filtered)) # Store x,y, raw and filtered values
        logging.info(f"Points ({x}, {y}) - Raw: {raw}, Filtered: {filtered}")

    # peak detection
    peak_value, peak_point = detect_peak(results)
    if peak_value is not None:
        logging.info(f"Detected peak value is {peak_value} at ({peak_point[0]} and {peak_point[1]})")
    else:
        logging.warning("No valid data to compute peak.")

    if return_peak: 
        return results, (peak_value, peak_point)
    else:
        return results
    

# Function to save result to csv
def save_to_csv(results, filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["x", "y", "raw_value", "filtered_value"])  # header
        for row in results:
            writer.writerow(row)


#Log and call the functions only when this file is run seperately
if __name__ == "__main__":
    base_path = os.path.abspath(os.path.dirname(__file__))
    # Create output/ folder before setting up logging
    os.makedirs(os.path.join(base_path, "output"), exist_ok=True)
    # logging configuration
    logging.basicConfig(
        level=getattr(logging, config["logging_level"]),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(base_path, "output", "scan.log"), mode= 'w')
        ]
    )

    # Example log
    logging.info("Scan controller started.")
    data, (peak_value, peak_point) = perform_scan(config, return_peak= True)
    save_to_csv(data, os.path.join(base_path, config["output_csv"]))
    logging.info(f"Scan data saved to {config['output_csv']}")

    # Write peak to CSV
    peak_csv_path = os.path.join(base_path, config["output_csv"])
    with open(peak_csv_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([])  # empty row for separation
        writer.writerow(["Peak Value", "X", "Y"])
        if peak_value is not None:
            writer.writerow([peak_value, peak_point[0], peak_point[1]])
        else:
            writer.writerow(["None", "None", "None"])

    logging.info(f"Peak value written to {config['output_csv']}")
    
