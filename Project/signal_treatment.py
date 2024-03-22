import matplotlib.pyplot as plt
import numpy as np
from scipy.signal.windows import hamming
from scipy import signal as sg

# Load the data
def load(id):
    """
    This function loads the data from a CSV file and plots the signal.

    Parameters:
    id (int): The column index to load from the CSV file.

    Returns:
    tuple: Returns a tuple containing the signal data, time data, and the sampling frequency (Fs).
    """
    # read the column at position id in the data/data.csv file
    signal = np.loadtxt('data/data.csv', delimiter=',', usecols=(id,))
    # Time is an array of every 10 ms for 10s
    time = [i*0.01 for i in range(1000)]

    # Plot the signal and force the scale to be from -1 to 1
    scale = max(signal) if max(signal) > abs(min(signal)) else abs(min(signal))
    scale *= 1.1
    plt.plot(time, signal, color='black', linewidth=1, label='selected signal 1')
    plt.ylim(-scale, scale)
    plt.show()

    dt = time[-1] - time[-2]
    Fs = np.ceil(1/np.round(dt,4))

    return signal, time, Fs

# Apply the Hamming window and the Butterworth filter
def signal_treatment():
    """
    This function applies the Hamming window and the Butterworth filter to the signal data.

    Returns:
    None
    """
    # Load the data
    [signal, time, Fs] = load(1)
    Nd = signal.size
    Sm = np.mean(signal) # Mean of the signal
    Sm_ = -Sm
    signal = signal + Sm_
    del Sm_

    # Hamming window
    frame_size = signal.size
    windowed_signal = hamming(frame_size, sym=True) * signal

    b, a = sg.butter(3,0.45, 'low', analog=False)
    zi = sg.lfilter_zi(b, a)
    z, _ = sg.lfilter(b, a, windowed_signal, zi=zi * windowed_signal[0])
    z2, _ = sg.lfilter(b, a, z, zi=zi * z[0])
    y = sg.filtfilt(b, a, windowed_signal)

    plt.plot(time, signal, color='c', linewidth=1, label='selected signal')
    plt.plot(time, windowed_signal, color='g', linewidth=1, label='windowed signal')
    plt.plot(time, y, color='r', linewidth=1, label='filtered signal')
    plt.legend()
    plt.show()

    return y, Nd, Fs, frame_size, time
