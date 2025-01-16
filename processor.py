import numpy as np
from scipy.fft import fft, fftfreq



def calculate_power_spectrum(time_series, sampling_rate):
    """Calculate the power spectrum of a time series."""
    n = len(time_series)
    yf = fft(time_series)
    xf = fftfreq(n, 1/sampling_rate)
    
    # Get positive frequencies only
    positive_freqs = xf[1:n//2]
    power_spectrum = 2.0/n * np.abs(yf[1:n//2])
    
    return positive_freqs, power_spectrum