import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from signal_t import signal_treatment
from scipy.signal import find_peaks

def compute_fft():
    """
    This function computes the Fast Fourier Transform (FFT) of the signal data.

    Returns:
    list: Returns a list of the first six non-zero frequencies in the FFT.
    """
    # Get the windowed signal, size of the signal, sampling frequency, and time array from the signal_treatment function
    [ws, Nd, Fs, _, t] = signal_treatment()

    # Compute the FFT of the windowed signal
    fhat = fft(ws, norm='forward')
    # Compute the frequency scale
    freq = fftfreq(len(ws))*Fs
    freq_l = np.arange(0, np.floor(ws.size / 2), dtype='int')

    # Define the time difference, height threshold, and distance for peak detection
    tt = 10
    height_threshold = max(np.abs(fhat[freq_l]))/tt
    dist = tt

    # Compute the prominence for peak detection
    prom = max(np.abs(fhat[freq_l]))/20

    # Find the peaks in the FFT
    peaks_index, properties = find_peaks(np.abs(fhat[freq_l]), height=height_threshold,  prominence=prom, distance=dist)

    # Get the frequencies corresponding to the peaks
    f_nf = freq[peaks_index]

    # Plot the FFT and the peaks
    plt.plot(freq, np.abs(fhat), '-', freq[peaks_index], np.abs(fhat[peaks_index]), 'x')
    plt.xlim(freq[freq_l[0]], 20)
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.show()

    # Return the first six non-zero frequencies
    return f_nf[0:6]