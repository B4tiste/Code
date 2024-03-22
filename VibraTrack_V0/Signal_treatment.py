import matplotlib.pyplot as plt
import numpy as np
from scipy.signal.windows import hamming
from scipy import signal
import os

# ---------------------------------------------------------------------------------------------------------------------
# Identify the current directory and import the signal
directory = os.getcwd()
print(directory)
# ---------------------------------------------------------------------------------------------------------------------
# Change the current working directory to the signal folder
name = "T17I_4.25.2023_16h23_FAC"
os.chdir(name)
# ---------------------------------------------------------------------------------------------------------------------
def load():
    # Signal parameters
    signal = np.loadtxt('Signal.dat', unpack=True)
    time = np.loadtxt('Time.dat', unpack=True)
    # plt.plot(time, signal, color='c', linewidth=1, label='selected signal')
    # plt.show()
    selected_signal = np.loadtxt('Selected_Signal.dat', unpack=True)
    selected_t = np.loadtxt('Selected_Time.dat', unpack=True)
    dt = time[100] - time[99]
    Fs = np.ceil(1/np.round(dt,4))
    # print(Fs)
    del signal, time

    return selected_signal, selected_t, dt, Fs
# ---------------------------------------------------------------------------------------------------------------------
def cursorlimits(selected_t, Fs):
    # Find cursor limits of selected signal
    Imin = selected_t[0] * Fs
    Imax = selected_t[-1] * Fs

    Nd = int(np.ceil(Imax)) - int(np.ceil(Imin))

    return Nd
# ---------------------------------------------------------------------------------------------------------------------
def signal_treatment():

    [selected_signal, selected_t, dt, Fs] = load()
    # Nd = cursorlimits(selected_t, Fs)
    Nd = selected_signal.size
    Sm = np.mean(selected_signal) # Mean of the signal
    Sm_ = -Sm
    selected_signal = selected_signal + Sm_
    del Sm_

    # ---------------------------------------------------------------------------------------------------------------------
    # Hamming window
    frame_size = selected_signal.size
    windowed_signal = hamming(frame_size, sym=True) * selected_signal

    b, a = signal.butter(3,0.45, 'low', analog=False)
    zi = signal.lfilter_zi(b, a)
    z, _ = signal.lfilter(b, a, windowed_signal, zi=zi * windowed_signal[0])
    z2, _ = signal.lfilter(b, a, z, zi=zi * z[0])
    y = signal.filtfilt(b, a, windowed_signal)

    # plt.plot(selected_t, selected_signal, color='c', linewidth=1, label='selected signal')
    # plt.plot(selected_t, windowed_signal, color='g', linewidth=1, label='windowed signal')
    # plt.plot(selected_t, y, color='r', linewidth=1, label='filtered signal')
    # plt.legend()
    # plt.show()


    return y, Nd, Fs, frame_size, selected_t
    # return windowed_signal, Nd, Fs, frame_size, selected_t


