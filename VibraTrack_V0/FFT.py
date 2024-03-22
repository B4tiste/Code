import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, ifft
from Signal_treatment import signal_treatment
from scipy.signal.windows import hamming, exponential
from scipy.signal import find_peaks_cwt, find_peaks
from spectrum import *
from pylab import *

def compute_fft():
    [ws, Nd, Fs, _, t] = signal_treatment()

    fhat = fft(ws, norm='forward')
    # The frequency scale
    freq = fftfreq(len(ws))*Fs
    freq_l = np.arange(0, np.floor(ws.size / 2), dtype='int')

    # Find the peaks with height_threshold >=0.01
    # Note: We use the magnitude (i.e the absolute value) of the Fourier transform
    # print('max_amplitude:', max(np.abs(fhat[freq_l])))


    # med_signal = scipy.signal.medfilt(np.abs(fhat[freq_l]), kernel_size=None)
    # print('med_amplitude:', max(med_signal)/6)
    # height_threshold = max(med_signal)/6  # six modes so divided by 6


    tt = (t[-1] - t[0])
    print('time diff:', tt)
    height_threshold = max(np.abs(fhat[freq_l]))/tt
    print('height:', height_threshold)
    dist = tt
    print('max_amplitude:', max(np.abs(fhat[freq_l])))


    print('height:', height_threshold)
    prom = max(np.abs(fhat[freq_l]))/20
    print('prom:', prom)

    # peaks_index contains the indices in x that correspond to peaks:
    peaks_index, properties = find_peaks(np.abs(fhat[freq_l]), height=height_threshold,  prominence=prom, distance=dist)
    # peaks_index += 1
    f_nf = freq[peaks_index]
    print('f_nf:', f_nf)

    plt.plot(freq, np.abs(fhat), '-', freq[peaks_index], np.abs(fhat[peaks_index]), 'x')
    plt.xlim(freq[freq_l[0]], 20)
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.show()


    cwt_peaks = fft_peak(tt, ws, Fs)
    f_cwt = freq[cwt_peaks]
    print('f_cwt:', f_cwt[0:6])


    # plt.plot(freq, np.abs(fhat), '-', freq[cwt_peaks[0:10]], np.abs(fhat[cwt_peaks[0:10]]), 'x')
    # plt.xlim(freq[freq_l[0]], 40)
    # plt.xlabel("Frequency")
    # plt.ylabel("Amplitude")
    # plt.show()
    return f_nf[0:6]

def fft_peak(tt,signal, Fs):
    fhat = fft(signal)
    freq = fftfreq(len(signal))*Fs
    freq_l = np.arange(0, np.floor(signal.size / 2), dtype='int')
    # cwt_peaks = find_peaks_cwt(np.abs(fhat[freq_l]), widths=np.arange(1,20), wavelet=None, max_distances=None,
    #                gap_thresh=None, min_length = tt/2,
    #                min_snr=2, noise_perc=10, window_size=None )
    cwt_peaks = find_peaks_cwt(np.abs(fhat[freq_l]), widths=np.arange(1,20), wavelet=None, max_distances=None,
                   gap_thresh=None, min_length=None,
                   min_snr=1, noise_perc=10, window_size=None)
    # cwt_peaks = find_peaks_cwt(np.abs(fhat[freq_l]), Fs/np.arange(1,10)/tt)
    # print('f0', f0[0:20])
    # plt.plot(np.abs(freq[freq_l]), np.abs(fhat[freq_l]), label='FFT')
    # plt.plot(np.abs(freq[freq_l[cwt_peaks]]), np.abs(fhat[freq_l[cwt_peaks]]), marker='x')
    # plt.legend()
    # plt.show()
    return cwt_peaks

