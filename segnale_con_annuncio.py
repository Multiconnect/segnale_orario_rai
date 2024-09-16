import numpy as np
import sounddevice as sd
from gtts import gTTS
from playsound import playsound
from datetime import datetime

def generate_tone(frequency, duration_ms, sample_rate):
    t = np.linspace(0, duration_ms / 1000.0, int(sample_rate * duration_ms / 1000.0), False)
    return 0.5 * np.sin(2 * np.pi * frequency * t)

sample_rate = 44100
tone_duration_ms = 30
impulse_duration_ms = 100
frequencies = [2000, 2500]
impulse_frequency = 1000

segment_52_53 = np.concatenate([
    np.concatenate([generate_tone(frequencies[0], tone_duration_ms, sample_rate),
                    generate_tone(frequencies[1], tone_duration_ms, sample_rate)])
    for _ in range(17)
])

impulses = np.concatenate([
    np.concatenate([generate_tone(impulse_frequency, impulse_duration_ms, sample_rate),
                    np.zeros(int(sample_rate * 0.9))])
    for _ in range(5)
])

last_impulse = np.concatenate([np.zeros(int(sample_rate)), generate_tone(impulse_frequency, impulse_duration_ms, sample_rate)])

full_signal = np.concatenate([segment_52_53, np.zeros(int(sample_rate)), impulses, last_impulse, np.zeros(int(sample_rate))])

sd.play(full_signal, sample_rate)
sd.wait()

current_time = datetime.now()
hour = current_time.hour
minute = current_time.minute

if hour == 0:
    if minute == 0:
        time_message = "È mezzanotte?"
    elif minute == 1:
        time_message = "È mezzanotte, e un minuto?"
    else:
        time_message = f"È mezzanotte, e {minute} minuti?"
elif hour == 1:
    if minute == 0:
        time_message = "È l'una?"
    elif minute == 1:
        time_message = "Sono le ore una, e un minuto?"
    else:
        time_message = f"Sono le ore una, e {minute} minuti?"
elif minute == 0:
    time_message = f"Sono le ore {hour}?"
elif minute == 1:
    time_message = f"Sono le ore {hour}, e un minuto?"
else:
    time_message = f"Sono le ore {hour}, e {minute} minuti?"

tts = gTTS(time_message, lang='it', slow=False)
tts.save("time_announcement.mp3")
playsound("time_announcement.mp3")
