import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import linalg
from fft import compute_fft

# Initialize the plot
def init_plot():
    # Plotting settings
    plt.style.use('ggplot')
    plt.rcParams['figure.figsize'] = [8, 6]
    plt.rcParams.update({'font.size': 10})
    plt.rcParams['lines.markersize'] ** 10

# Read the cable characteristics
def read_cable_characteristics():
    # vib_data from courses
    data = pd.read_excel(r"data\Data_Hernani.xlsx")
    df = data.loc[0]
    # Cable_name = data.iloc[0][0]
    # System_type = data.loc[0][1]
    # Sensor_position = data.loc[0][2] #[m]
    # Number_of_strands = data.loc[0][3]
    # Cable_mass  = data.loc[0][4] #[kg/m]
    # Inclination = data.loc[0][5] #[deg]
    # Eff_cross_section = data.loc[0][6] #[mm2]
    # Length_BP2BP = data.loc[0][7] #[m] Length btw the two bearing plates
    # Transition_length_pylon = data.loc[0][8] #[mm]
    # Transition_length_deck = data.loc[0][9] #[mm]
    # Deviator_pylon = data.loc[0][10]
    # Deviator_deck = data.loc[0][11]
    # Deviator_pos_pylon = data.loc[0][12] #[m]
    # Deviator_pos_deck = data.loc[0][13] #[m]
    # Estimated_tension = data.loc[0][14] #[kN]
    # E_modulus = data.loc[0][15] #[GPa]
    # Diameter = data.loc[0][16] #[mm]
    # Air_density = data.loc[0][17] #[kg/m3]
    # free_length = 42.14 #[m]
    # print (df)

    return df

# Determine the free length
def free_length_determination():
    df = read_cable_characteristics()
    # Check if there is a deviator at pylon
    if df.iloc[10] == 'None':
        Deviation_P = 0
        Deviator_P = Deviation_P * df.iloc[12]
        Transition_length_P = df.iloc[8] * 10e-3 #[m]
    else:
        Deviation_P = 1
        Deviator_P = Deviation_P * df.iloc[12]
        Transition_length_P = 0

    # Check if there is a deviator at deck
    if df.iloc[11] == 'None':
        Deviation_D = 0
        Deviator_D = Deviation_D * df.iloc[13]
        Transition_length_D = df.iloc[9] * 10e-3 #[m]
    else:
        Deviation_D = 1
        Deviator_D = Deviation_D * df.iloc[13]
        Transition_length_D = 0

    # Free length
    free_length = df.iloc[7] - Deviator_P - Deviator_D - Transition_length_P - Transition_length_D

    return df, free_length

# Least square fit
def leastsquare(x, A, B): # least-square-fit
    return A * x + B

# Estimated frequency
def estimated_frequency_first(df, free_length, n = 1):
    # For n = 1
    cs_area = df.iloc[6]*1e-6 #[m2]
    inclination = np.deg2rad(df.iloc[5])
    Est_tension = df.iloc[14] * 1000  # [N]
    # Est_tension = (4*math.pow(free_length, 2)*math.pow((f_estimated[0]/1), 2))*df[4]
    f_fft = compute_fft()

    F0 = f_fft  # Dominant frequency
    f_estimated = (n / (2 * free_length)) * np.sqrt(Est_tension / df.iloc[4])
    lambda2_top = df.iloc[15] * 1e9 * cs_area * (df.iloc[4] * 9.81 * free_length * np.cos(inclination))**2
    lambda2 = lambda2_top/math.pow(Est_tension,3)
    f_corrected = f_estimated / np.sqrt(1 + ((8 * lambda2)/(n * np.pi)**4))
    return F0, f_corrected, f_fft

# Calculate the tension
def calculate_tension():
    df, free_length = free_length_determination()
    free_length = 42.14
    A1 = 1 / (4 * df.iloc[4] * free_length ** 2)
    [F0, f_corrected, f_estimated] = estimated_frequency_first(df, free_length, n=1)
    num_of_modes = len(F0)
    matrix_tension = np.zeros((num_of_modes, 2))
    matrix_f = np.zeros((num_of_modes, 1))
    # print(F0)
    for i in range(num_of_modes):
        A2 = ((i + 1) ** 2 * np.pi ** 2) * (A1)
        if (i == 0):
            f_n = (f_corrected / (i + 1)) ** 2
        else:
            f_n = ((F0[i]) / (i + 1)) ** 2
        matrix_tension[i, :] = [A1, A2]
        matrix_f[i] = f_n
    out = np.matmul(linalg.pinv(matrix_tension), matrix_f)
    tension = out[0] / 1000  # [kN]
    EI = out[1] * 1e6

    print('Tension' , tension, 'EI', EI, 'f0', f_corrected, 'f_n', f_estimated)
    return tension

if __name__ == '__main__':
    calculate_tension()