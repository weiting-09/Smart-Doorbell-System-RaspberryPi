from time import sleep

CL = [0, 131, 147, 165, 175, 196, 220, 247]
CM = [0, 262, 294, 330, 349, 392, 440, 494]
CH = [0, 523, 587, 659, 698, 784, 880, 988]

melody_doorBell = [CH[3], CH[1]]
beat_doorBell = [1, 2]

def play_doorbell_chime(Buzz):
    Buzz.start(50)
    for i in range(len(melody_doorBell)):
        Buzz.ChangeFrequency(melody_doorBell[i])
        sleep(beat_doorBell[i] * 0.5)
    Buzz.stop()

