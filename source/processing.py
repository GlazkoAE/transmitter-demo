from scipy.signal import upfirdn
from scipy.signal import welch


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


def parce_real_imag(data: list[int], bytes_per_sample=1):
    i_samples = []
    q_samples = []
    for sample_start_index in range(0, len(data), 2 * bytes_per_sample):
        i_last = sample_start_index + bytes_per_sample
        q_last = sample_start_index + bytes_per_sample * 2
        i_sig = data[sample_start_index:i_last]
        q_sig = data[i_last:q_last]
        i_samples += parse_samples(i_sig, bytes_per_sample)
        q_samples += parse_samples(q_sig, bytes_per_sample)
    return i_samples, q_samples


def filter_signal(signal, coefficients, sps):
    return upfirdn(coefficients, signal[1:], up=1, down=sps)


def psd(x, fs, nperseg=256):
    f, pxx = welch(x, fs, nperseg=nperseg)
    return f, pxx
