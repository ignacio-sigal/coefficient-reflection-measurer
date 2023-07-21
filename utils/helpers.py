import pyaudio
import numpy as np
from scipy import fft
from enum import Enum
from utils.constants import RATE, S, DIST, PI, C


class PlotOptions(Enum):
    """
    Different plot options
    """
    REFLECTION_COEFFICIENT = 0
    ABSORPTION_COEFFICIENT = 1


def process_raw_data(f, input_data: type(np.array)) -> tuple[type(np.array), type(np.array)]:
    """
    This function process the microphone input signal and calculates the fast fourier
    transform along with the reflection coefficient for each frequency.
    :param f:
    :param input_data:
    :return: reflection_coefficient, y_fft
    """
    y_fft = fft.fft(input_data[:, 0])
    y_fft2 = fft.fft(input_data[:, 1])

    y_fft = fft.fftshift(y_fft / RATE)
    y_fft2 = fft.fftshift(y_fft2 / RATE)

    k0 = 2 * PI * f / C

    hi = np.exp(-1j * k0 * S)
    hr = np.exp(1j * k0 * S)
    h12 = y_fft / y_fft2
    reflection_coefficient = ((h12 - hi) / (hr - h12)) * np.exp(2 * 1j * k0 * DIST)
    return reflection_coefficient, y_fft


def get_input_output_devices_names() -> list:
    """
    Return audio devices names.
    """
    device_list = []
    p = pyaudio.PyAudio()
    for i in range(0, 10):
        print(i, p.get_device_info_by_index(i)['name'])
        device_list.append(p.get_device_info_by_index(i)['name'])
    return device_list


def decode(data, chunk, channels):
    """
    Convert a byte stream into a 2D numpy array with
    shape (chunk_size, channels)

    Samples are interleaved, so for a stereo stream with left channel
    of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the output
    is ordered as [L0, R0, L1, R1, ...]
    """
    result = np.fromstring(data, dtype=np.float32)

    result = np.reshape(result, (chunk, channels))
    return result
