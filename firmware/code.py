import board
import analogio
import digitalio
import pwmio
import synthio
import audiopwmio
import usb_midi
import time
import array

# pins
stylus = analogio.AnalogIn(board.GP26)
decay_knob = analogio.AnalogIn(board.GP27)
led = pwmio.PWMOut(board.GP2, frequency=1000, duty_cycle=0)

btn_oct = digitalio.DigitalInOut(board.GP4)
btn_oct.direction = digitalio.Direction.INPUT
btn_oct.pull = digitalio.Pull.UP

btn_wav = digitalio.DigitalInOut(board.GP5)
btn_wav.direction = digitalio.Direction.INPUT
btn_wav.pull = digitalio.Pull.UP

# audio
audio = audiopwmio.PWMAudioOut(board.GP0)
synth = synthio.Synthesizer(sample_rate=22050)
audio.play(synth)

# waveforms 256 samples each
# range is -32768 to 32767
square = array.array("h", [0] * 256)
for i in range(256):
    if i < 128:
        square[i] = 32767
    else:
        square[i] = -32768

saw = array.array("h", [0] * 256)
for i in range(256):
    saw[i] = int(i * 65535 / 256 - 32768)

# found online how to make a triangle wave
triangle = array.array("h", [0] * 256)
for i in range(256):
    if i < 128:
        triangle[i] = int(i * 65535 / 128 - 32768)
    else:
        triangle[i] = int((256 - i) * 65535 / 128 - 32768)

waves = [square, saw, triangle]
wave_names = ["square", "saw", "triangle"]

# C4 to G5
midi_notes = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
              70, 71, 72, 73, 74, 75, 76, 77, 78, 79]

def midi_to_freq(midi):
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))

# midi output
midi_port = usb_midi.ports[1]

def midi_on(note):
    midi_port.write(bytes([0x90, note, 100]))

def midi_off(note):
    midi_port.write(bytes([0x80, note, 0]))

# state
current_pad = 0
playing = False
fading = False
fade_start = 0
current_note = None
current_midi = 0
octave = 0
wave_idx = 0
prev_oct = True
prev_wav = True

def read_pad():
    raw = stylus.value
    step = 65535 / 21
    pad = round(raw / step)
    # uncomment to debug pad readings:
    # print("raw:", raw, "pad:", pad)
    if pad < 1 or pad > 20:
        return 0
    return pad

def read_decay():
    raw = decay_knob.value
    return 0.05 + (raw / 65535) * 1.95

print("starting...")

while True:
    pad = read_pad()

    # False means pressed for buttons
    oct_now = btn_oct.value
    wav_now = btn_wav.value

    if oct_now == False and prev_oct == True:
        octave = octave + 1
        if octave > 1:
            octave = -1
        print("octave:", octave)
    prev_oct = oct_now

    if wav_now == False and prev_wav == True:
        wave_idx = wave_idx + 1
        if wave_idx > 2:
            wave_idx = 0
        print("wave:", wave_names[wave_idx])
        if current_note is not None and playing:
            current_note.waveform = waves[wave_idx]
    prev_wav = wav_now

    if pad > 0 and not playing:
        # new note
        # if we were still fading from the last note, kill it first
        if fading and current_note is not None:
            synth.release(current_note)
            led.duty_cycle = 0
            fading = False

        midi_num = midi_notes[pad - 1] + (octave * 12)
        freq = midi_to_freq(midi_num)
        current_note = synthio.Note(frequency=freq, waveform=waves[wave_idx])
        synth.press(current_note)
        led.duty_cycle = 65535
        playing = True
        current_pad = pad
        current_midi = midi_num
        midi_on(midi_num)
        # print("playing pad", pad, "freq", freq)

    elif pad > 0 and playing and pad != current_pad:
        # sliding between pads
        old_midi = current_midi
        midi_num = midi_notes[pad - 1] + (octave * 12)
        current_note.frequency = midi_to_freq(midi_num)
        current_pad = pad
        current_midi = midi_num
        midi_off(old_midi)
        midi_on(midi_num)

    elif pad == 0 and playing:
        # lifted stylus, start fading
        playing = False
        fading = True
        fade_start = time.monotonic()
        midi_off(current_midi)

    # fade the led down after lifting
    if fading:
        decay_time = read_decay()
        elapsed = time.monotonic() - fade_start
        if elapsed >= decay_time:
            led.duty_cycle = 0
            fading = False
            if current_note is not None:
                synth.release(current_note)
                current_note = None
            current_pad = 0
        else:
            bright = 1.0 - (elapsed / decay_time)
            led.duty_cycle = int(bright * 65535)

    time.sleep(0.005)