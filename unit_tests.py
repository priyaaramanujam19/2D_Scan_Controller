import unittest
import logging
from unittest.mock import patch
from functions import measure_sensor, sensor, stage, move_stage
from scan_controller import compute_rolling_average, detect_peak, generate_scan_points
logging.disable(logging.CRITICAL)
# Tests for measure sensor
@patch.object(sensor, 'measure') # mocking the sensor
class TestMeasureSensor(unittest.TestCase):
    # Sensor works immediately, no retries needed
    def test_measure_success_on_first_try(self, mock_measure): #Test case(TC) 1
        mock_measure.return_value = 1.23
        max_retries = 2
        x, y = 5, 10  # dummy x and y for testing
        result = measure_sensor(x, y, max_retries)
        self.assertEqual(result, 1.23)

    # Sensor fails once (None), should succeed on retry
    def test_measure_none_then_success(self, mock_measure): # TC 2
        mock_measure.side_effect = [None, 1.23]
        max_retires = 3
        x, y = 5, 10  # dummy x and y for testing
        result = measure_sensor(x,y,max_retires)
        self.assertEqual(result, 1.23)

    # Sensor fails all attempts (raises ValueError), should return None
    def test_measure_fails_all_attempts(self, mock_measure): #TC 3
        mock_measure.side_effect = ValueError()
        max_retires = 3
        x, y = 5, 10  # dummy x and y for testing
        result = measure_sensor(x,y,max_retires)
        self.assertIsNone(result)

# Tests for move stage
@patch.object(stage, 'move_to') # mocking the stage
class TestMoveStage(unittest.TestCase):

    # Move succeeds on first attempt, so should return True
    def test_move_success_on_first_try(self, mock_move): # TC 4
        mock_move.return_value = None  # no exception → success
        x = 1
        y = 2
        max_retires = 2
        result = move_stage(x, y, max_retires)
        self.assertTrue(result)

    # Move fails every time, should return False and also check the number of retries
    def test_move_fails_all_attempts(self, mock_move): #TC 5
        mock_move.side_effect = TimeoutError()
        x = 1
        y = 2
        max_retires = 2
        result = move_stage(x, y, max_retires)
        self.assertFalse(result)
        self.assertEqual(mock_move.call_count, 2)

# Tests for rolling average
class Testrollingaverage(unittest.TestCase):
    #pass three values one by one
    def testrollingaverage(self): #TC 6
        window_size= 2
        recent_values = []
        result = compute_rolling_average(recent_values, 10.0, window_size)
        self.assertEqual(result, 10.0)

        # Second value
        result = compute_rolling_average(recent_values, 20.0, window_size)
        self.assertEqual(result, 15.0)

        # Third value
        result = compute_rolling_average(recent_values, 30.0, window_size)
        self.assertEqual(result, 25.0)       
    # pass a list of values
    def test_rolling_average_from_list(self): #TC 7
        window_size = 2
        values = [10.0, 20.0, 30.0, 40.0]
        expected_outputs = [10.0, 15.0, 25.0, 35.0]
        recent_values = []
        for new_value, expected in zip(values, expected_outputs):
            result = compute_rolling_average(recent_values, new_value, window_size)
            self.assertEqual(result, expected)

## peak detection tests
class testpeakdetection(unittest.TestCase): 
    #pass a list of tuples with x,y,raw,filtered values, should return peak value and point
    def test_peak_detected_correctly(self): #TC 8
        results= [ 
            (0, 0, 1.0, 11.0),
            (1, 0, 2.0, 2.5),
            (2, 0, 3.0, 3.0),  # peak value = 11.5
            (3, 0, 2.5, 2.5),
            (4, 0, 0.5, 11.5)
        ]
        peak_value, peak_point = detect_peak(results)
        self.assertEqual(peak_value, 11.5)
        self.assertEqual(peak_point,(4,0))
    # pass a list of tuples with none values, should return none
    def test_peak_none(self): #TC 8
        results =[
            (0,25,None,None),
            (1,25,None,None),
            (2,25,None,None)]
        peak_value, peak_point = detect_peak(results)
        self.assertIsNone(peak_value)
        self.assertIsNone(peak_point)
    # edge case to handle both none and valid values
    def test_single_peak(self): #TC 8
        results = [
            (0,25,None,None),
            (1,25,12,12),
            (2,25,None,None)]
        peak_value, peak_point = detect_peak(results)
        self.assertEqual(peak_value,12)
        self.assertEqual(peak_point,(1,25))

#Test zig zag pattern scan points generation
class scanpointstest(unittest.TestCase):
    # pass x and y range, should return expected pattern
    def testscanpoints(self):  #TC 8
        x_range={"start": 0, "end": 50,"steps": 3}
        y_range = {"start": 0, "end": 50,"steps": 3}
        points = generate_scan_points(x_range,y_range)
        expected_points = [(0,0), (25,0), (50,0),
                           (50,25), (25,25), (0,25),
                           (0,50), (25,50), (50,50)]
        self.assertEqual(points,expected_points )


if __name__ == "__main__":
    unittest.main()
