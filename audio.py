import sounddevice as sd
import numpy as np

SOUND_AMPLITUDE = 0
AUDIO_CHEAT = 0

CALLBACKS_PER_SECOND = 38               
SUS_FINDING_FREQUENCY = 2               
SOUND_AMPLITUDE_THRESHOLD = 20         

FRAMES_COUNT = int(CALLBACKS_PER_SECOND/SUS_FINDING_FREQUENCY)
AMPLITUDE_LIST = list([0]*FRAMES_COUNT)
SUS_COUNT = 0
count = 0

def print_sound(indata, outdata, frames, time, status):
    avg_amp = 0
    global SOUND_AMPLITUDE, SUS_COUNT, count, SOUND_AMPLITUDE_THRESHOLD, AUDIO_CHEAT
    vnorm = int(np.linalg.norm(indata)*10)
    AMPLITUDE_LIST.append(vnorm)
    count += 1
    AMPLITUDE_LIST.pop(0)
    if count == FRAMES_COUNT:
        avg_amp = sum(AMPLITUDE_LIST)/FRAMES_COUNT
        SOUND_AMPLITUDE = avg_amp
        if SUS_COUNT >= 2:
            AUDIO_CHEAT = 1
            SUS_COUNT = 0
        if avg_amp > SOUND_AMPLITUDE_THRESHOLD:
            SUS_COUNT += 1
        else:
            SUS_COUNT = 0
            AUDIO_CHEAT = 0
        count = 0

def sound():
    with sd.Stream(callback=print_sound):
        sd.sleep(-1)

def sound_analysis():
    global AMPLITUDE_LIST, FRAMES_COUNT, SOUND_AMPLITUDE
    while True:
        AMPLITUDE_LIST.append(SOUND_AMPLITUDE)
        AMPLITUDE_LIST.pop(0)

        avg_amp = sum(AMPLITUDE_LIST)/FRAMES_COUNT

        if avg_amp > 10:
            print("Sus...")

if __name__ == "__main__":
    sound()