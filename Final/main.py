import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import linalg
from fft_utils import compute_fft

def init_plot():
    # Plotting settings
    plt.style.use('ggplot')
    plt.rcParams['figure.figsize'] = [8, 6]
    plt.rcParams.update({'font.size': 10})
    plt.rcParams['lines.markersize'] ** 10

def get_cable_specs(cableId, data="data/STAY_CABLES_DATA.xlsx"):
    """
    This function reads the cable specifications from the data file.

    Args:
    cableId (int): The cable ID.
    data (str): The path to the data file.

    Returns:
    pandas.core.series.Series: Returns a pandas series of the cable specifications.
    """

    # Read the cable data
    cable_data = pd.read_excel(data)
    cableId += 4

    # Get the cable specifications
    """ Cable specs ids :
    0 : Cable_ID
    1 : Cable_name
    2 : Cable_Inclination_alpha
    3 : Cable_free_length_L
    4 : Young_Modolus_E
    5 : Effective_steel_Cross_section_Ac
    6 : Distributed_mass_at_anchorage_exit_ma
    7 : Distributed_mass_in_free_length_mc (Cable Mass)
    8 : Cable_Inertia_at_anchorage_exit_Ia
    10 : Initial_estimated_T0
    """
    cable_specs = {
        "Incline": cable_data.loc[cableId].iloc[2],
        "Length": cable_data.loc[cableId].iloc[3],
        "E": cable_data.loc[cableId].iloc[4],
        "Ac": cable_data.loc[cableId].iloc[5],
        "Mass": cable_data.loc[cableId].iloc[7],
        "T0": cable_data.loc[cableId].iloc[10]
    }

    return cable_specs

def estimated_frequencies(cable_specs):
    """
    This function calculates the estimated frequency of the cable using the fft.

    Args:
    cable_specs (pandas.core.series.Series): The cable specifications.

    Returns:
    list: Returns a list of the estimated frequencies.
    """

    # Get the cable specifications
    incline = cable_specs["Incline"]
    length = cable_specs["Length"]
    E = cable_specs["E"]
    ac = cable_specs["Ac"]
    mass = cable_specs["Mass"]
    T0 = cable_specs["T0"]

    f_fft = compute_fft()

    F0 = f_fft
    f_estimated = (1 / (2 * length)) * np.sqrt(T0 / mass)
    lambda2_top = E * 1e9 * ac * (mass * 9.81 * length * np.cos(incline))**2
    lambda2 = lambda2_top/math.pow(T0,3)
    f_corrected = f_estimated / np.sqrt(1 + ((8 * lambda2)/np.pi**4))

    return F0, f_corrected, f_fft

def calculate_tension(cable_specs):
    """
    This function calculates the tension in the cable.

    Args:
    cable_specs (pandas.core.series.Series): The cable specifications.

    Returns:
    float: Returns the tension in the cable.
    """

    # Get the cable specifications
    """ Cable specs ids :
    0 : Cable_ID
    1 : Cable_name
    2 : Cable_Inclination_alpha
    3 : Cable_free_length_L
    4 : Young_Modolus_E
    5 : Effective_steel_Cross_section_Ac
    6 : Distributed_mass_at_anchorage_exit_ma
    7 : Distributed_mass_in_free_length_mc (Cable Mass)
    8 : Cable_Inertia_at_anchorage_exit_Ia
    10 : Initial_estimated_T0
    """

    length = cable_specs["Length"]
    mass = cable_specs["Mass"]

    A1 = 1 / (4 * mass * length ** 2)
    [F0, f_corrected, f_estimated] = estimated_frequencies(cable_specs)

    num_of_modes = len(F0)
    matrix_tension = np.zeros((num_of_modes, 2))
    matrix_f = np.zeros((num_of_modes, 1))

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

    print(f"Tension: {tension} kN, EI: {EI}, f0: {f_corrected}, f_n: {f_estimated}")
    return tension

if __name__ == '__main__':
    init_plot()

    calculate_tension(get_cable_specs(1))