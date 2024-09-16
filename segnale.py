import numpy as np
import sounddevice as sd

sample_rate = 44100
tone_duration_ms = 30
total_segment_duration_sec = 1
impulse_duration_ms = 100
frequencies = [2000, 2500]
impulse_frequency = 1000

def generate_tone(frequency, duration_ms, sample_rate):
    duration_sec = duration_ms / 1000.0
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    return 0.5 * np.sin(2 * np.pi * frequency * t)

segment_52_53 = np.concatenate([
    np.concatenate([generate_tone(frequencies[0], tone_duration_ms, sample_rate),
                    generate_tone(frequencies[1], tone_duration_ms, sample_rate)])
    for _ in range(int(total_segment_duration_sec * 1000 / (tone_duration_ms * 2)))
])

impulses = np.concatenate([
    np.concatenate([generate_tone(impulse_frequency, impulse_duration_ms, sample_rate),
                    np.zeros(int(sample_rate * (1 - impulse_duration_ms / 1000)))])
    for _ in range(5)
])

last_impulse = np.concatenate([np.zeros(int(sample_rate)), generate_tone(impulse_frequency, impulse_duration_ms, sample_rate)])

full_signal = np.concatenate([segment_52_53, np.zeros(int(sample_rate)), impulses, last_impulse, np.zeros(int(sample_rate))])

sd.play(full_signal, sample_rate)
sd.wait()
