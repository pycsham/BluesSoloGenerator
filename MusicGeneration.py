import random
import music21

class BluesMusicGeneration:
    # chord sequence is currently default to the classical blues chord sequence and the C major scale
    # This version only uses the rhythmic structure of the CFG and overlays the blues scale on top of it
    def __init__(self, sequence, key="C", chordSequence=[1,1,1,1,4,4,1,1,5,5,1,1]):
        self.sequence = sequence # the sequence produced by the CFG 
        self.key = key # a string that represents which key we're working with 
        self.chordSequence = chordSequence # the chord sequence, where each element in the list represents chord per bar
        self.result = music21.stream.Stream() # the result stream of notes
        self.pianoChordsTrack = music21.stream.Stream() # Stores the chords being played as the "Left hand side"
        self.guitarChordsTrack = music21.stream.Stream() # guitar chords track
        self.barSequence = []
        self.bluesScale = {
            "C": ["C", "D#", "F", "F#", "G", "A#"],
            "A": ["A", "C", "D", "D#", "E", "G"],
            "A+C": ["C", "D", "D#", "E", "F", "F#", "G", "A", "A#"]
        }
        self.direction = "up"
        self.octave = random.randint(1,7)
        self.newScale = random.choice(["A", "C", "A+C"])
        self.newNote = random.randint(0, len(self.bluesScale[self.newScale]))

        
        # self.chordsMap = {
        #     1: 'C3 E3 G3 A#3',
        #     4: 'C3 D#3 F3 A3',
        #     5: 'D3 F3 G3 B3'
        # }

        # for c in self.chordSequence:
        #     chordNotes = self.chordsMap[c]
        #     for i in range(2):
        #         duration = music21.duration.Duration(2.0)
        #         chord = music21.chord.Chord(chordNotes, duration=duration)
        #         self.pianoChordsTrack.append(chord)

        #         duration1 = music21.duration.Duration(1.5)
        #         duration2 = music21.duration.Duration(0.5)
        #         chord1 = music21.chord.Chord(chordNotes, duration=duration1)
        #         chord2 = music21.chord.Chord(chordNotes, duration=duration2)
        #         self.guitarChordsTrack.append(chord1)
        #         self.guitarChordsTrack.append(chord2)
        
        # fp = self.pianoChordsTrack.write('midi', fp="./results/pianoChordsTrack.midi")
        # fg = self.guitarChordsTrack.write('midi', fp="./results/guitarChordsTrack.midi")
       

        # Mapping the rhythm to duration, using the convention in music21
        self.rhythmMap = {
            "1": 4,
            "2": 2,
            "4": 1,
            "4.": 1.5,
            "8": 0.5,
            "16": 0.25,
            "4/3": 2.0/3.0,
            "8/3": 1.0/3.0,
            "16/3": 1.0/6.0
        }


        # Mapping each note in the sequence from a string to a tuple (pitch, rhythm)
        for index,note in enumerate(sequence):
            self.sequence[index] = (note[0], note[1:])

        # Categorize the sequence into bars according to rhythm
        curBeats = 0
        bar = []
        index = 0
        while index < len(self.sequence):
            s = self.sequence[index]
            r = s[1]
            #  New Bar
            if curBeats >= 4: #There could be carry over from the previous bar
                curBeats = curBeats - 4
                self.barSequence.append(bar)
                bar = []

            if r == "4/3" or r == "8/3" or r == "16/3": # Consider a group of triplets, assume these don't stride across bars
                if r[0] == "4":
                    curBeats += 2
                elif r[0] == "8":
                    curBeats += 1
                else:
                    curBeats += 0.5
                for i in range(3):
                    bar.append(self.sequence[index+i])
                index += 3
            else:
                bar.append(self.sequence[index])
                index += 1
                curBeats += self.rhythmMap[r]
        if bar:
            self.barSequence.append(bar)
        


            


    # Maps the sequence into a stream of notes 
    # Simply using the rhythmic skeleton for now
    # Rules:
    # 1. Going up or down the blues scale 
    # 2. When to decide a new "direction":
    #    A rest
    #    Bounds of keys
    #    Chord change
    #    Repeated triplets could play the same sequence 
    #    After a longer note (a 2 or 1)
    # 3. A new direction: 
    #    randomly choose a new octave (from the one above, below and the same one)
    #    choose the note on the blues scale to start on 
    


    def switchDirection(self):
        print("direction switched")
        if self.direction == "up":
            self.direction = "down"
        else:
            self.direction = "up"
        
        # Randomly choose a new octave
        octaves = [self.octave]
        if self.octave > 1:
            octaves.append(self.octave-1)
        if self.octave < 7:
            octaves.append(self.octave+1)
        self.octave = random.choice(octaves)

        # Chooses a new note on the blues scale to start on
        # Currently only choosing from the C blues scale
        self.newScale = random.choice(["A", "C", "A+C"])
        self.newNote = random.randint(0,len(self.bluesScale[self.newScale])-1)


    def generate(self, filename):
        for index, bar in enumerate(self.barSequence):
            # Switching directions if there is a chord change
            if index > 0 and self.sequence[index-1] != self.sequence[index]:
                self.switchDirection()
            for note in bar:
                duration = self.rhythmMap[note[1]]
                if note[0] == "R":
                    self.result.append(music21.note.Rest(quarterLength=duration))
                    self.switchDirection()
                else:
                    self.result.append(music21.note.Note(self.bluesScale[self.newScale][self.newNote%len(self.bluesScale[self.newScale])]+str(self.octave), quarterLength=duration))
                    # Switching direction if after a long note
                    if duration == 4 or duration == 2 or duration == 1.5:
                        self.switchDirection()
                    
                    # Generating the next note's octave and newNote
                    if self.direction == "up":
                        if self.newNote >= 5:
                            if self.octave < 7:
                                self.octave += 1
                            else:
                                self.switchDirection()
                        
                        self.newNote = (self.newNote+1)%len(self.bluesScale[self.newScale]) # "circular" on the blues scale
                    else:
                        if self.newNote <= 0:
                            if self.octave > 1:
                                self.octave -= 1
                            else:
                                self.switchDirection()
                        self.newNote = (self.newNote-1)%len(self.bluesScale[self.newScale])

        self.result.write('midi', fp="./results/default.midi")
        return
    






                


       





    