from scipy.signal import upfirdn
from scipy.signal import welch
from math import log10


def parse_bytes_reversed(sample, bytes_num):
    res = 0
    for index, reversed_index in enumerate(reversed(range(bytes_num))):
        coeff = 2 ** (8 * index)
        res += sample[reversed_index] * coeff
    return res


def parse_bytes(sample, bytes_num):
    res = 0
    for index in range(bytes_num):
        coeff = 2 ** (8 * index)
        res += sample[index] * coeff
    return res


def parse_samples(signal, bytes_num):
    sample = []
    res = []
    for byte in signal:
        sample.append(byte)
        if len(sample) == bytes_num:
            res.append(parse_bytes(sample, bytes_num))
            sample = []
    return res


def parce_real_imag(data):
    i_samples = data[0:-1:2]
    q_samples = data[1:-1:2]
    return i_samples, q_samples


def filter_signal(signal, coefficients, sps):
    return upfirdn(coefficients, signal[0:], up=1, down=1)


def psd(real, imag, fs, nperseg=256):
    sample = [x + y * 1j for x, y in zip(real, imag)]
    f, pxx = welch(sample, fs, nperseg=nperseg, nfft=1024)
    pxx = [10*log10(x) for x in pxx]
    f = [*f[int(len(f)/2):], *f[:int(len(f)/2)]]
    pxx = [*pxx[int(len(pxx)/2):], *pxx[:int(len(pxx)/2)]]
    return f, pxx
