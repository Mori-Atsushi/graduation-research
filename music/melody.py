# -*- coding:utf-8 -*-

import numpy as np

class Melody:
    def __init__(self):
        self.__chordMelody = np.zeros((60, 12))
        self.__chordMelody += 0.01
        for i in range(0, len(self.__chordMelody)):
            self.__chordMelody[i][i / 5] = 0.31
            x = i % 5
            if x == 0:
                self.__chordMelody[i][(i / 5 + 4) % 12] = 0.3
                self.__chordMelody[i][(i / 5 + 7) % 12] = 0.3
            elif x == 1:
                self.__chordMelody[i][(i / 5 + 3) % 12] = 0.3
                self.__chordMelody[i][(i / 5 + 7) % 12] = 0.3
            elif x == 2:
                self.__chordMelody[i][(i / 5 + 4) % 12] = 0.3
                self.__chordMelody[i][(i / 5 + 8) % 12] = 0.3
            elif x == 3:
                self.__chordMelody[i][(i / 5 + 3) % 12] = 0.3
                self.__chordMelody[i][(i / 5 + 6) % 12] = 0.3
            else:
                self.__chordMelody[i][(i / 5 + 5) % 12] = 0.3
                self.__chordMelody[i][(i / 5 + 7) % 12] = 0.3
                
    def calcEmissionProbability(self, measure):
        emisson_probability = np.zeros(62)
        i = 0
        for chord in self.__chordMelody:
            emisson_probability[i + 1] = np.dot(chord, measure)
            i += 1
        return emisson_probability

if __name__ == '__main__':
    melody = Melody()
    phrase = np.array([
        [ 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [ 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ])
    for measure in phrase:
        melody.calcEmissionProbability(measure)