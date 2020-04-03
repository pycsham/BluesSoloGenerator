from random import choice
import music21

class BluesMusicGeneration:
    # chord sequence is currently default to the classical blues chord sequence and the E major scale
    def __init__(self, sequence, key="E", chordSequence=[1,1,1,1,4,4,1,1,5,5,1,1]):
        self.sequence = sequence # the sequence produced by the CFG 
        self.key = key # a string that represents which key we're working with 
        self.chordSequence = chordSequence # the chord sequence, where each element in the list represents chord per bar
        self.result = music21.stream.Stream() # the result stream of notes
        self.octave = ["3","4","5","6"] 

        # The following are dictionaries of the form: int -> set(str) where the key represents a chord, and the set of string represents a set of notes

        # Chords: taking the dominant 7th chords
        self.chordTone = {
            1: ["E", "G#", "B", "D"],
            4: ["A", "C#", "E", "G"],
            5: ["B", "D#", "F#", "A"]
        }
        # The 9th, 11th and 13th notes of each chord (extended jazz chords)
        self.colorTone = {
            1: ["F#", "A", "C#"],
            4: ["B", "D", "F#"],
            5: ["C#", "E", "A#"]
        }

        # Taking the Diatonic-Chromatic Enclosure approach
        # (diatonic above, chromatic below)
        # Note: these are not necessarily scale tones since it's chromatic below
        self.approachTone = {
            1: {
                "E": ["D#", "F#"],
                "G#": ["G", "A"],
                "B": ["A#", "C#"],
                "D": ["C#", "E"],
                "F#": ["F", "G#"],
                "A": ["G#", "B"],
                "C#": ["C", "D#"]
            },
            4: {
                "A": ["G#", "B"],
                "C#":["C", "D"],
                "E":["D#", "F#"],
                "G":["F#", "A"],
                "B":["A#", "C#"],
                "D":["C#", "E"],
                "F#":["F", "G#"]
            },
            5: {
                "B":["A#", ""],
                "D#":["D", "E"],
                "F#":["F", "G#"],
                "A":["G#", "B"],
                "C#":["C", "D#"],
                "E": ["D#", "F#"],
                "A#": ["A", "B"]
            }
        }
        # Taking the major blues scale since we're assuming the underlying chords are major 7th
        # The major blues scale: R-2-b3-3-5-6 (not too sure about this, it's supposed to be soronous to the current chord?)
        self.scaleTone = {
            1: ["E", "F#", "G", "G#", "B", "C#"],
            4: ["A", "B", "C", "C#", "E", "F#"],
            5: ["B", "C#", "D", "D#", "F#", "G#"]
        } 

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


        # Mapping each note in the sequence from a string to a tuple (rhythm, pitch) 
        for index,note in enumerate(sequence):
            self.sequence[index] = (note[0], note[1:])




    # Generates a chord tone , color tone, or scale tone note
    def generateChordColorScaleNote(self, chord, tone, duration):
        pitch = ""
        if tone == "C":
            pitch = choice(self.chordTone[chord])
        elif tone == "L":
            pitch = choice(self.colorTone[chord])
        elif tone == "S":
            pitch = choice(self.scaleTone[chord])
        
        octave = choice(self.octave)
        self.result.append(music21.note.Note(pitch+octave, quarterLength=duration))
    
    # Generates an appraoch tone (forces the next note to be a chord tone)
    def generateApproachNote(self, chord, duration, curBeats):
        try:
            nextSymbol = self.sequence.pop(0)
        except: # reached the end of the sequence (this is most likely impossible given the grammar)
            # Since we've reached the end of the sequence, it makes sense for the last note to be a chord tone
            self.generateChordColorScaleNote(chord, "C", duration)
            return
        
        # Forcing the next note to be a chord tone
        print(nextSymbol)
        nextDuration = self.rhythmMap[nextSymbol[1]]
        nextPitch = choice(self.chordTone[chord])
        

        pitch = choice(self.approachTone[chord][nextPitch])
        octave = choice(self.octave)
        self.result.append(music21.note.Note(pitch+octave, quarterLength=duration))

        # Currently default the next chord tone to be in the same octave 
        # TODO: adjust the octave according to the enclosure rules in the approach tone
        self.result.append(music21.note.Note(nextPitch+octave, quarterLength=nextDuration))
        curBeats += nextDuration        


    # Maps the sequence into a stream of notes 
    def generate(self, filename):
        curBeats = 0 # keeping track of the number of beats
        for chord in self.chordSequence:
            if curBeats > 4:
                curBeats = curBeats - 4
            elif curBeats == 4:
                curBeats = 0
            print("chord is : {}".format(chord))
            while curBeats < 4:
                try:
                    curSymbol = self.sequence.pop(0) # this is because of the "striding across bars" #TODO: fix this issue
                except:
                    break
                print(curSymbol)
                pitch = curSymbol[0]
                duration = self.rhythmMap[curSymbol[1]]

                # Appending the next note to the result
                if pitch == "R": # Rest
                    self.result.append(music21.note.Rest(quarterLength=duration))
                elif pitch == "C" or pitch == "S" or pitch == "L":
                    self.generateChordColorScaleNote(chord, pitch, duration)
                elif pitch == "A": # approach tone (forces the next note to be a chord tone)
                    self.generateApproachNote(chord, duration, curBeats)
                elif pitch == "H": # one of chord tone, color tone or approach tone
                    pitch = choice(["C", "L", "A"])
                    if pitch == "A":
                        self.generateApproachNote(chord, duration, curBeats)
                    else:
                        self.generateChordColorScaleNote(chord, pitch, duration)
                elif pitch == "X": # could be any tone
                    pitch = choice(["C", "L", "A", "S"])
                    if pitch == "A":
                        self.generateApproachNote(chord, duration, curBeats)
                    else:
                        self.generateChordColorScaleNote(chord,pitch,duration)
                
                # Updating the curBeats
                curBeats += duration
                    
        
        
        fp = self.result.write('midi', fp="./results/"+filename)
    






                


       





    