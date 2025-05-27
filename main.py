import sounddevice as sd
import numpy as np
import subprocess
import time
import math

SAMPLE_RATE = 44100
DURATION = 0.01
LOW_FREQ_CUTOFF = 85.5
DEVICE_INDEX = 22
MIN_DB = 22.7
MAX_DB = 29.5
CURVA_EXP = 3.5

def set_led(state):
    cmd = ["xset", "led", "named", "Scroll Lock"] if state else ["xset", "-led", "named", "Scroll Lock"]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def process_audio(indata):
    audio = indata[:, 0]
    window = np.hamming(len(audio))
    audio = audio * window
    fft = np.abs(np.fft.rfft(audio))
    freqs = np.fft.rfftfreq(len(audio), d=1/SAMPLE_RATE)
    graves = fft[freqs < LOW_FREQ_CUTOFF]
    energia_db = np.mean(20 * np.log10(graves + 1e-6))
    return energia_db

def map_brightness(energia_db):
    normalized = (energia_db - MIN_DB) / (MAX_DB - MIN_DB)
    brilho = math.exp(CURVA_EXP * normalized) - 1
    brilho_max = math.exp(CURVA_EXP) - 1
    return max(0.0, min(1.0, brilho / brilho_max))

try:
    with sd.InputStream(device=DEVICE_INDEX, channels=1, samplerate=SAMPLE_RATE,
                        blocksize=int(SAMPLE_RATE * DURATION)) as stream:
        while True:
            data, _ = stream.read(int(SAMPLE_RATE * DURATION))
            energia = process_audio(data)

            brilho = map_brightness(energia)
            brilho_percent = brilho * 100

            if brilho <= 0:
                set_led(False)
                print(f"{energia:.1f} dB | brilho: {brilho_percent:.1f}%       ", end="\r")
                continue

            # boa sorte tentando ajustar isso caso no seu teclado nao funcione :)
            on_time = brilho**2 * 0.0001 
            off_time = max(0.001, 0.0001 - on_time)

            print(f"{energia:.1f} dB | brilho: {brilho_percent:.1f}%         ", end="\r")

            set_led(True)
            time.sleep(on_time)
            set_led(False)
            time.sleep(off_time)

except KeyboardInterrupt:
    set_led(False)

