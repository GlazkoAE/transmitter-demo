from scipy.signal import upfirdn
from scipy.signal import welch


def parce_real_imag(data: list[int], sps: int):
    i_sig = []
    q_sig = []
    for sample_start_index in range(0, len(data), sps * 2):
        i_last = sample_start_index + sps
        q_last = sample_start_index + sps * 2
        i_sig += data[sample_start_index:i_last]
        q_sig += data[i_last:q_last]
    return i_sig, q_sig


def filter_signal(signal, coefficients, sps):
    # not tested!!!
    # check last or first value (mb in plot)
    return upfirdn(coefficients, signal, up=1, down=sps)


def psd(x, fs, nperseg=256):
    f, pxx = welch(x, fs, nperseg=nperseg)
    return f, pxx
