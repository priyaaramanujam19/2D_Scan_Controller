import logging
import time
from sim_devices import SimStage, SimSensor
from sim_devices import SimStage, SimSensor
from config import load_yaml_file

stage = SimStage()
sensor = SimSensor()
config = load_yaml_file()

#Function to move stage with retries
def move_stage(x,y,retries_max): 
    for tries in range(retries_max):
        try:
            stage.move_to(x,y)
            logging.info(f"Stage moved to ({x}, {y}) on attempt {tries + 1}")
            return True
        except TimeoutError as error:
            logging.warning(f"Move failed at attempt {tries + 1}: {error}")
            time.sleep(1)
    else:
        logging.critical(f"Stage move failed after {retries_max} attempts")
        return False

#Function to measure sensor with retries
def measure_sensor(x,y,retries_max):
    for tries in range(retries_max):
        try:
            value = sensor.measure()
            if value is None:
                raise ValueError("Received no value from the sensor")
            logging.info(f"Sensor measured value: {value}")
            return value
        except ValueError as error:
            logging.warning(f"Measurement failed at attempt {tries + 1}: {error} at ({x},{y}) ")
            time.sleep(1)
    else:
        logging.error(f"Sensor measurement failed after {retries_max} attempts.")
        return None
