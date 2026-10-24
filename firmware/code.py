import board
import analogio
import pwmio
import synthio
import audiopwmio
import time
import array

# basic pad reading and sound output test

stylus = analogio.AnalogIn(board.GP26)
led = pwmio.PWMOut(board.GP2, frequency=1000, duty_cycle=0)

audio = audiopwmio.PWMAudioOut(board.GP0)
synth = synthio.Synthesizer(sample_rate=22050)
audio.play(synth)

# square wave
square = array.array("h", [0] * 256)
for i in range(256):
    if i < 128:
        square[i] = 32767
    else:
        square[i] = -32768

# notes C4 to G5 in midi
midi_notes = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
              70, 71, 72, 73, 74, 75, 76, 77, 78, 79]

def midi_to_freq(midi):
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))

current_note = None
current_pad = 0

def read_pad():
    raw = stylus.value
    step = 65535 / 21
    pad = round(raw / step)
    if pad < 1 or pad > 20:
        return 0
    return pad

print("testing stylus...")

while True:
    pad = read_pad()
    raw = stylus.value
    print("raw:", raw, "pad:", pad)

    if pad > 0 and current_pad == 0:
        # touched
        midi_num = midi_notes[pad - 1]
        freq = midi_to_freq(midi_num)
        print("  -> playing", freq, "hz")
        current_note = synthio.Note(frequency=freq, waveform=square)
        synth.press(current_note)
        led.duty_cycle = 65535
        current_pad = pad

    elif pad > 0 and pad != current_pad:
        # moved to different pad
        midi_num = midi_notes[pad - 1]
        freq = midi_to_freq(midi_num)
        print("  -> slide to", freq, "hz")
        current_note.frequency = freq
        current_pad = pad

    elif pad == 0 and current_pad > 0:
        # lifted
        print("  -> off")
        synth.release(current_note)
        current_note = None
        led.duty_cycle = 0
        current_pad = 0

    time.sleep(0.01)