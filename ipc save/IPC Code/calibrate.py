import numpy as np
from scipy.integrate import trapezoid
import math


## TEST - Acceleration calibration ##
def calibrate_acceleration(x_raw, z_raw, max_cross_axis_sensitivity, sensitivity_x, sensitivity_z):
    """
    Calculates calibrated acceleration values for a two-axis sensor considering sensitivity coefficients
    and max cross-axis sensitivity.

    Args:
    raw_values: Raw acceleration values from the sensor.
    sensitivity_coeffs: Sensitivity coefficients for each axis.
    max_cross_axis_sensitivity: Maximum cross-axis sensitivity factor as a percentage.

    Returns:
    Calibrated acceleration values for each axis.
    """
    # Calculate the calibrated acceleration values
    x_calibrated = x_raw * (1 + max_cross_axis_sensitivity * z_raw / sensitivity_x)
    z_calibrated = z_raw * (1 + max_cross_axis_sensitivity * x_raw / sensitivity_z)
    return x_calibrated, z_calibrated

# Example
x_raw = 1  # Raw acceleration value in x-axis [g]
z_raw = 0.5  # Raw acceleration value in z-axis [g]
max_cross_axis_sensitivity = 0.01  # Maximum cross-axis sensitivity 1%
sensitivity_x = 0.5  # Sensitivity in x-axis [V/g]
sensitivity_z = 0.5  # Sensitivity in z-axis [V/g]

x_calibrated, z_calibrated = calibrate_acceleration(x_raw, z_raw, max_cross_axis_sensitivity, sensitivity_x,
                                                    sensitivity_z)

print("Calibrated acceleration in x-axis:", x_calibrated)
print("Calibrated acceleration in z-axis:", z_calibrated)


def matrix_multiplication(matrix1, matrix2):
    if len(matrix1[0]) != len(matrix2):
        return "Matrix multiplication not possible"

    result = [[0] for _ in range(len(matrix1))]
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

    return result

## TEST - Integrate over time ##

# Assuming time is sampled at regular intervals
time = np.linspace(0, 10, 1000)  # 10 seconds, sampled 1000 times
acceleration_x = np.sin(time)  # Example acceleration signal in x-direction (sin wave)
acceleration_z = np.cos(time)  # Example acceleration signal in z-direction (cos wave)

# Define the time period over which to integrate
start_time = 2.0  # Start time for integration (seconds)
end_time = 8.0  # End time for integration (seconds)

# Find indices corresponding to start and end times
start_index = np.argmax(time >= start_time)
end_index = np.argmax(time >= end_time)

# Integrate acceleration over the specified time period using trapezoidal rule
average_acceleration_x = trapezoid(acceleration_x[start_index:end_index], time[start_index:end_index]) / (
            end_time - start_time)
average_acceleration_z = trapezoid(acceleration_z[start_index:end_index], time[start_index:end_index]) / (
            end_time - start_time)

print("Average acceleration in x-direction over the period:", average_acceleration_x)
print("Average acceleration in z-direction over the period:", average_acceleration_z)

## TEST - Find cable and sensor inclination ##
# Calculate the sensor inclination angle in radians
sensor_inclination_rad = math.atan2(average_acceleration_z, average_acceleration_x)
# Convert radians to degrees
sensor_inclination_deg = math.degrees(sensor_inclination_rad)
print("Sensor inclination angle [deg]:", sensor_inclination_deg)

# Calculate the cable inclination angle in radians
magnitude_OF_acceleration = np.sqrt(average_acceleration_x ** 2 + average_acceleration_z ** 2)
cable_inclination_rad = math.acos(magnitude_OF_acceleration / 9.81)
# Convert radians to degrees
cable_inclination_deg = math.degrees(cable_inclination_rad)
print("Cable inclination angle [deg]:", cable_inclination_deg)

## TEST - Find vertical and horizontal acceleration values using sensor_inclination_angle ##

orientation_matrix = [[math.cos(sensor_inclination_rad), math.sin(sensor_inclination_rad)],
                      [-math.sin(sensor_inclination_rad), math.cos(sensor_inclination_rad)]]
calibrated_acc = [[x_calibrated],
                  [z_calibrated]]

acc = matrix_multiplication(orientation_matrix,calibrated_acc)
print("acceleration values in vertical direction", acc[0])
print("acceleration values in horizontal direction", acc[1])


