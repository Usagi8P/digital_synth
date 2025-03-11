import pyaudio
import math
import itertools
import numpy as np

def main():
    C4 = 261.6255
    E4 = 329.63
    G4 = 392.00
    SAMPLE_RATE = 44_100
    INT16_CONVERSION = (2**15-1)


    stream = pyaudio.PyAudio().open(
        rate=44100,
        channels=1,
        format=pyaudio.paInt16,
        output=True,
        frames_per_buffer=100
    )

    # c4samples = np.sin(np.arange(stop=60000, step=(2 * np.pi * C4) / SAMPLE_RATE))
    # e4samples = np.sin(np.arange(stop=60000, step=(2 * np.pi * E4) / SAMPLE_RATE))
    # g4samples = np.sin(np.arange(stop=60000, step=(2 * np.pi * G4) / SAMPLE_RATE))
    # smallest_array = min(len(c4samples),len(e4samples),len(g4samples))-1
    # # normalized = ((c4samples[:smallest_array]+e4samples[:smallest_array]+g4samples[:smallest_array]) - np.min((c4samples[:smallest_array]+e4samples[:smallest_array]+g4samples[:smallest_array]))) / (np.max((c4samples[:smallest_array]+e4samples[:smallest_array]+g4samples[:smallest_array])) - np.min((c4samples[:smallest_array]+e4samples[:smallest_array]+g4samples[:smallest_array])))
    # normalized = ((c4samples[:smallest_array]+e4samples[:smallest_array]+g4samples[:smallest_array]) / (np.max(np.abs(c4samples[:smallest_array]+e4samples[:smallest_array]+g4samples[:smallest_array]))))
    # samples = normalized*INT16_CONVERSION
    # # print(samples)
    # samples = samples.astype(np.int16)
    # stream.write(samples)

    c4_oscilator = get_sin_oscillator(C4, sample_rate=SAMPLE_RATE)
    e4_oscilator = get_sin_oscillator(E4, sample_rate=SAMPLE_RATE)
    g4_oscilator = get_sin_oscillator(G4, sample_rate=SAMPLE_RATE)
    c4_oscilator = get_squ_oscilator(c4_oscilator)
    e4_oscilator = get_squ_oscilator(e4_oscilator)
    g4_oscilator = get_squ_oscilator(g4_oscilator)
    playing = True
    n_loops = 0
    i = 0
    while playing:
        c4_samples = np.array([next(c4_oscilator) for _ in range(256)])
        e4_samples = np.array([next(e4_oscilator) for _ in range(256)])
        g4_samples = np.array([next(g4_oscilator) for _ in range(256)])
        samples = normalize(c4_samples,e4_samples,g4_samples) * .2

        samples = samples * INT16_CONVERSION
        samples = samples.astype(np.int16).tobytes()


        stream.write(samples)


def normalize(*arrays) -> np.array:
    final_array = np.sum(np.array(arrays),axis=0)
    final_array = final_array / len(arrays)
    return final_array


def get_sin_oscillator(freq: float = 261.6255, amp: float = 1, phase: float = 0, sample_rate: int = 256):
    phase = (phase / 360) * 2 * np.pi
    increment = (2 * np.pi * freq) / sample_rate
    return (np.sin(v + phase) * amp for v in itertools.count(start=0, step=increment))


def get_squ_oscilator(oscilator):
    return (np.sign(v) for v in oscilator)


if __name__ == "__main__":
    main()