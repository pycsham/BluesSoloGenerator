from random import choice
import music21

class BluesMusicGeneration:
    # chord sequence is currently default to the classical blues chord sequence and the C major scale
    # This version only uses the rhythmic structure of the CFG and overlays the blues scale on top of it
    def __init__(self, sequence, key="C", chordSequence=[1,1,1,1,4,4,1,1,5,5,1,1]):
        self.sequence = sequence # the sequence produced by the CFG 
        self.key = key # a string that represents which key we're working with 
        self.chordSequence = chordSequence # the chord sequence, where each element in the list represents chord per bar
        self.result = music21.stream.Stream() # the result stream of notes
        self.chordsTrack = music21.stream.Stream() # Stores the chords being played as the "Left hand side"
        self.barSequence = []
        
        # self.chordsMap = {
        #     1: 'C3 E3 G3 A#3',
        #     4: 'C3 D#3 F3 A3',
        #     5: 'D3 F3 G3 B3'
        # }

        # for c in self.chordSequence:
        #     chordNotes = self.chordsMap[c]
        #     for i in range(3):
        #         duration = music21.duration.Duration(2.0)
        #         chord = music21.chord.Chord(chordNotes, duration=duration)
        #         self.chordsTrack.append(chord)
        
        # fp = self.chordsTrack.write('midi', fp="./results/chordsTrack.midi")
       

        # Mapping the rhythm to duration, using the convention in music21
        self.rhythmMap = {
            "1": 4,
            "2": 2,
            "4": 1,
            "4.": 1.5,
            "8": 0.5,
            "16": 0.25
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
    def generate(self, filename):
        



                    
        
        
        # fp = self.result.write('midi', fp="./results/"+filename)
        return
    






                


       





    