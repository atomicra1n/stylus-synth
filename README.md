# Stylus Synthesizer

A small synthesizer played with a stylus or a probe (such as a multimeter one). It has 20 copper pads on the PCB acting as a keyboard, a speaker and a headphone jack. Controlled by an RP2040-Zero featuring an analog vactrol circuit.

<img width="1788" height="1869" alt="image" src="https://github.com/user-attachments/assets/04ea2737-80d3-41f2-b3a6-b4045d41d5ff" />

<img width="2466" height="1710" alt="image" src="https://github.com/user-attachments/assets/0cff34d1-e5db-4b84-b4c4-d026eaa7899a" />

<img width="1824" height="1874" alt="image" src="https://github.com/user-attachments/assets/a8bcf560-3d54-4eb0-8004-33711a93fc07" />

## Features

- 20 note keyboard (note C to G) from exposed copper pads, playable with a conductive stylus
- Notes fade out naturally when the stylus is lifted (thanks to the Vactrol circuit, LED + photoresistor)
- Volume and decay knobs
- Octave button and waveform button (supports square wave, saw wave and triangle wave)
- Speaker and a headphone jack that automatically turns the speaker off when headphones are plugged in
- Can also act as a USB MIDI controller
- Fully through-hole, easy to solder

## Motivation

Week 3 of Hack Club's Half Life was all about music. I remembered an interesting musical instrument from the 60s, which had small metal pads that would play notes when touched with a stylus (the Stylophone), so I decided to make my own smaller version. I also added a small vactrol circuit to make it sound more natural instead of notes cutting off.

## Functionality

- The keyboard has a chain of 21 1 kiloohm resistors between ground and 3.3 volts. Each pad is between two resistors, so it has a different voltage than the rest. The stylus goes into an ADC pin of the RP2040, so it can easily tell all 20 pads apart with just one pin. 
- The RP2040 produces sound as a fast PWM on the GP0 pin, so there are two low-pass filters (1 kiloohm resistor + 10 nanoFarad capacitor each) that smooth it into a waveform
- The vactrol circuit is simply a green LED shining on a photoresistor. They are sealed together with black heat-shrink. Together they make a filter that opens when the LED is on, and when the stylus lifts, the LED fades and the photoresistor slowly recovers in the dark. This means the note slowly gets quieter and more dull. If it doesn't work right, there is a jumper to bypass the vactrol circuit. 
- A 10 microFarad capacitor removes 1.65V DC from the PWM and two 100 kiloohm resistors make the signal smaller for the amplifier. There is a 10 kiloohm potentiometer for volume.
- The LM386 amp increases the signal 20 times and runs off 5V from the USB. 
- The headphone jack has a switch inside. Because the speaker goes through said switch, it turns off when the headphones plug in.

## How it was made

Everything was designed in KiCad. As I couldn't check my work gradually, I ran simulations in [Falstad](https://www.falstad.com/circuit/) to check values for the PWM and vactrol. Some issues that arised:

- The RP2040-Zero had no footprint, so I had to make my own, which was a bit tricky due to spacing between pins.
- The headphone jack I originally found on GM Electronic had no datasheet so I had no clue what the pinout was. I needed to switch to the ST-214C which did have one. 
- The datasheet I found for the potentiometers had a very blurry drawing which was hard to understand, so I had to make it out with quite the difficulty. I figured out the potentiometers seemingly mount sideways, meaning the knobs stick out the back edge. I also needed to watch the pin order, otherwise the knobs would turn the wrong way.
- I originally planned to add resistors in series with the headphone jack to make the headphones a bit quieter, but figured out that the resistors would also end up in the speaker path and make it way too quiet. So I made it that the volume knob controls both.
- I originally routed the amp input too long around the board which would introduce a lot of noise (the amp boosts all signal 20 times).

## Tech stack

- KiCad for the schematic and PCB
- Falstad for simulating the PWM and vactrol paths
- CircuitPython and synthio library for the firmware
- JLCPCB for board manufacturing, GM Electronic for components

## Repo layout

- pcb/ contains all the KiCad work (PCB, schematic, symbols, footprints...)
- pcb/gerbers contains the gerber and drill files
- firmware/ contains the CircuitPython firmware
- images/ contains renders, schematic, PCB layout and Falstad simulations
- BOM.csv contains the bill of materials

## Bill of materials

| Part | Qty | Source | Unit | Total |
|---|---|---|---|---|
| [CREATALL RP2040-Zero](https://www.gme.cz/v/1518920/creatall-rp2040-zero-vyvojovy-modul-dual-core-cortex-m0-2-mb-flash) | 1 | GM Electronic | $5.50 | $5.50 |
| [LM386N-1 amplifier](https://www.gme.cz/v/1487657/texas-instruments-lm386n-1-nopb-zesilovac) | 1 | GM Electronic | $1.40 | $1.40 |
| [DIL08PZ Socket](https://www.gme.cz/v/1501853/kls-dil08pz-patice) | 1 | GM Electronic | $0.40 | $0.40 |
| [Speaker (PSR-29N08S)](https://www.gme.cz/v/1498665/hitpoint-psr-29n08s-yhq-reproduktor) | 1 | GM Electronic | $0.85 | $0.85 |
| [Potentiometer (PC1621NBK010)](https://www.gme.cz/v/1494558/pc1621nbk010-potenciometr) | 2 | GM Electronic | $1.00 | $2.00 |
| [KN32 knob](https://www.gme.cz/v/1500373/kn32-knoflik-plastovy-prumer-266mm-osa-6mm-cerny) | 2 | GM Electronic | $0.70 | $1.40 |
| [ST-214C 3.5mm jack](https://www.gme.cz/v/1501907/st-214c-jack-35-stereo) | 1 | GM Electronic | $0.55 | $0.55 |
| [TS6601 button](https://www.gme.cz/v/1497943/kls-ts6601-43-180-mikrospinac) | 2 | GM Electronic | $0.11 | $0.22 |
| [S140C 1x40 pin header](https://www.gme.cz/v/1514383/s140c-bila-kolikova-lista-1x40pin-roztec-254mm) | 1 | GM Electronic | $0.40 | $0.40 |
| [2 layer 100x100 mm PCB (5 pieces)](https://jlcpcb.com/) | 1 | JLCPCB | $4.00 | $4.00 |
| [Black heat-shrink tubing CHS21-6.4](https://www.gme.cz/v/1519087/c-tie-chs21-64-smrstovaci-buzirka) | 1 | GM Electronic | $0.55 | $0.55 |
| [Resistor 1 kiloohm 1% 0207](https://www.gme.cz/v/1486228/gym-cym-rm-1k-06w-1-0207-metalizovany-rezistor) | 23 | GM Electronic | $0.09 | $2.07 |
| [Resistor 1 Megaohm 1% 0207](https://www.gme.cz/v/1486816/gym-cym-rm-1m-06w-1-0207-metalizovany-rezistor) | 10 | GM Electronic | $0.09 | $0.90 |
| [Resistor 100 kiloohm 1% 0207](https://www.gme.cz/v/1494147/gym-cym-rm-100k-06w-1-0207-metalizovany-rezistor) | 10 | GM Electronic | $0.09 | $0.90 |
| [Resistor 10 ohm 1% 0207](https://www.gme.cz/v/1494152/gym-cym-rm-10r-06w-1-0207-metalizovany-rezistor) | 10 | GM Electronic | $0.09 | $0.90 |
| [Resistor 330 ohm 1% 0207](https://www.gme.cz/v/1494116/gym-cym-rm-330r-06w-1-0207-metalizovany-rezistor) | 10 | GM Electronic | $0.09 | $0.90 |
| [Capacitor 220 microFarad 25V](https://www.gme.cz/v/1484171/jamicon-ce-220u-25vit-jam-tl-8x115-rm35-bulk-elektrolyticky-kondenzator) | 5 | GM Electronic | $0.04 | $0.20 |
| [Capacitor 10 microFarad 16V](https://www.gme.cz/v/1486104/hitano-ce-10u-16vit-hit-exr-5x11-rm2-bulk-elektrolyticky-kondenzator) | 6 | GM Electronic | $0.13 | $0.78 |
| [Capacitor 100 nanofarad](https://www.gme.cz/v/1489676/hitano-ck-100n-50v-x7r-rm508-10-keramicky-kondenzator) | 3 | GM Electronic | $0.25 | $0.75 |
| [Capacitor 10 nanofarad](https://www.gme.cz/v/1489673/hitano-ck-10n-50v-x7r-rm508-10-keramicky-kondenzator) | 5 | GM Electronic | $0.16 | $0.80 |
| [Capacitor 47 nanofarad](https://www.gme.cz/v/1486853/hitano-ck-47n-50v-x7r-rm508-10-keramicky-kondenzator) | 6 | GM Electronic | $0.13 | $0.78 |
| [Green LED 5mm L-53SGC](https://www.gme.cz/v/1491527/kingbright-l-53sgc-led-5mm-zelena) | 2 | GM Electronic | $0.15 | $0.30 |
| [Photoresistor LDR5516](https://www.gme.cz/v/1495847/ldr5516-fotorezistor) | 1 | GM Electronic | $0.33 | $0.33 |
| [Jumper cap](https://www.gme.cz/v/1499579/kls-jumper-black-zkratovaci-propojka) | 1 | GM Electronic | $0.10 | $0.10 |
| [Stranded wire 0.5mm2, pack of 5m](https://www.gme.cz/v/1512382/elektrokabel-cya-1x05-cerveny-h05v-k-izolovany-vodic-lanko) | 5 | GM Electronic | $0.15 | $0.75 |
| **Parts subtotal** | | | | **$27.73** |
| Shipping (estimate) | | | | $10.00 |
| **Total** | | | | **$37.73** |

The stylus is intentionally missing from the BOM. You can solder a multimeter probe or similar and it should work just fine.
The total is over the 30$ budget of tier 1 funding, I will cover the rest out of pocket. 

## Assembly

- Order the PCB from JLCPCB using the gerber files and order the components from any electronic store or GM Electronic if you're Czech.
- Begin with the resistors. Keep in mind all resistors in the resistor ladder (above the keyboard) are 1 kiloohm.
- Solder the ceramic capacitors, the DIP-8 socket, the buttons and pin headers.
- Solder the electrolytic capacitors (be very careful about the polarity, longer leg goes into +!)
- Solder the potentiometers and headphone jack on the back edge
- Solder the RP2040-Zero onto the pin headers. The USB should face the back edge.
- Put the LM386 amp in the socket matching the silkscreen.
- For the vactrol, try to bend the LED and photoresistor to make them face each other. Slide heat-shrink over both and shrink it to avoid any light getting in from outside.
- Solder two wires from the speaker to the SPEAKER pads.
- Solder the stylus wire (your multimeter probe or similar) to the STYLUS pad.
- Put the jumper on JP1 pin 2 and 3. This turns the vactrol on. If it sounds weird, you can move it to 1-2 and it will be bypassed.

## Firmware

- Download CircuitPython for the Waveshare RP2040-Zero [here](https://circuitpython.org/board/waveshare_rp2040_zero/).
- Hold the BOOT button on the RP2040, plug in the USB and drag the .uf2 file onto the drive that should show up in your system.
- When the CIRCUITPY drive shows up in your system, copy over firmware/code.py onto it.

## Controls

- Touch a pad with the stylus to play it or slide between pads to change notes.
- VOLUME knob controls the volume, DECAY controls notes fading.
- OCTAVE button switches between -1, 0 and 1 octave.
- WAVE button toggles square, saw or triangle wave.

## AI disclosure
LLMs (Claude Opus 5.5) was used to get feedback on the PCB schematic and routing, review parts of it and help with fixing bugs. It was also used for other tedious but simple tasks, such as adding the BOM to this README. AI was not used in writing the README, Journal or other parts of the project.

---
 
Built for [Hack Club Half Life](https://halflife.hackclub.com/) Week 3 (Music).
