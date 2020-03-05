from CFG import CFG


def main():

    # Creating a CFG for the list of terminal symbols representing the generated 12 bars blues
    BlueSoloTerminals = {"X2", "X4", "X4.", "X8", "X16", "X4/3", "X8/3", 
                        "H2", "H4", "H4.", "H8", "H16", "H4/3", 'H8/3',
                        "A4", "A8", "A16", "A8/3", "C2", "C4", "C8",
                        "L4", "L8", "R4", "R8", "S4", "S8"}
    BlueSoloProduction = {
        "Q4": [[["Q2","V4","V4"], 52],
                [["V8", "N4", "N4", "N4", "V8"], 1],
                [["V4", "Q2", "V4"], 47]
        ],
        "Q2": [[["N2"], 6],
                [["V4", "V4"], 60],
                [["V8", "N4", "V8"], 12],
                [["H4.", "N8"], 16],
                [["H4/3", "H4/3", "H4/3"], 6]
        ],
        "Q1":[[["C4"], 100]
        ],
        "V4":[[["N4"], 22],
            [["V8", "V8"], 72],
            [["H8/3", "H8/3", "H8/3"], 5],
            [["H8/3", "H8/3", "A8/3"], 1]
        ],
        "V8": [[["N8"], 99],
                [["H16", "A16"], 1]
        ],
        "N2": [[["C2"], 100],
        ],
        "N4": [[["C4"], 34],
                [["L4"], 14],
                [["S4"], 34],
                [["N4"], 1],
                [["R4"], 17]
            ], # normalizeed values
        "N8": [[["C8"], 36],
                [["L8"], 18],
                [["S8"], 36],
                [["A8"], 1],
                [["R8"], 9]
        ] # normalizeed values           
    }
    BlueSoloCFG = CFG(BlueSoloTerminals, BlueSoloProduction)

    # First generate a high level skeleton 
    skeleton = BlueSoloCFG.generateSkeleton(48)
    print(skeleton)

    # Then Generate the sequence of rhythms and notes
    termSequence = BlueSoloCFG.generate(skeleton)
    print(termSequence)

    

main()