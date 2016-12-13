# -*- coding:utf-8 -*-

import numpy as np
import os.path
import re

class Melody:
    def __init__(self, songFolder, scoreFolder):
        self.__chordMelody = np.zeros((60, 12))
        self.__chordMelody += 0.01

        i = 1
        while True:
            songFilename = songFolder + '/' + str(i) + '.txt'
            if not os.path.exists(songFilename):
                break
            scoreFilename = scoreFolder + '/' + str(i) + '.mid'
            if not os.path.exists(scoreFilename):
                break
            i += 1

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

    def __analyze(self, songFilename, scoreFilename):
        midi_data = pretty_midi.PrettyMIDI(scoreFilename)
        tempo = midi_data.get_tempo_changes()[1][0]
        chroma_data = midi_data.get_chroma(tempo)
        key = '#0'
        re_key = re.compile(r'^//[#b][0-9]$')
        re_rest = re.compile(r'^[0-9]+$')
        i = 0
        for line in open(songFilename, 'r'):
            if line.startswith('//'):
                if re_key.match(line):
                    key = line[2:]
                continue
            cellArray = line.split('|')
            cellArray.pop()
            for cell in cellArray:
                if re_rest.match(cell):
                    i += int(cell) * 240
                else:
                    chordArray = cell.split(' ')
                    x = 240 / len(chordArray)
                    temp = i
                    j = i + x
                    for chord in chordArray:
                        print i
                        print chord
                        a = 1
                        melody_data = np.zeros(x)
                        for data in chroma_data[:,i:j]:
                            b = 0
                            for belo in data:
                                if belo > 0:
                                    melody_data[b] = a
                                b += 1
                            a += 1
                        print melody_data
                        i += x
                        j += x
                    i = temp + 240
                
    def calcEmissionProbability(self, measure):
        emisson_probability = np.zeros(62)
        i = 0
        for chord in self.__chordMelody:
            emisson_probability[i + 1] = np.dot(chord, measure)
            i += 1
        emisson_probability /= emisson_probability.sum()
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