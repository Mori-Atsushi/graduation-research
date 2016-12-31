# -*- coding:utf-8 -*-

import numpy as np
import os.path
import re
import pretty_midi

class Melody:
    def __init__(self, states):
        self.__n_states = len(states)
        self.__chordMelody = np.zeros((self.__n_states - 2, 12))
        self.__re_chord = []
        self.__re_triad = []
        chordList = [r'C|B#', r'C#|Db', r'D', r'D#|Eb', r'E|Fb', r'F|E#', r'F#|Gb', r'G', r'G#|Ab', r'A', r'A#|Bb', r'B|Cb']
        triadList = [r'', r'm', r'7?aug', r'7?dim', r'7?sus4']
        i = 0
        for item in chordList:
            self.__re_chord.append(re.compile(r'^(' + item + r')($|[^#b])'))
            self.__re_triad.append([])
            for triad in triadList:
                self.__re_triad[i].append(re.compile(r'^(' + item + r')' + triad))
            i += 1

    def analyze(self, chordFilename, melodyFilename):
        chordMelody = np.zeros((self.__n_states - 2, 12))
        midi_data = pretty_midi.PrettyMIDI(melodyFilename)
        tempo = midi_data.get_tempo_changes()[1][0]
        chroma_data = midi_data.get_chroma(tempo)
        keyNum = '0'
        re_key = re.compile(r'^//[#b][0-9]$')
        re_rest = re.compile(r'^[0-9]+$')
        i = 0
        for line in open(chordFilename, 'r'):
            if line.startswith('//'):
                if re_key.match(line):
                    key = line[2:]
                    keyNum = self.__getKeyNum(key)
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
                        chord_id = self.__replaceChord(keyNum, chord) - 1
                        a = 0
                        for data in chroma_data[:,i:j]:
                            for belo in data:
                                if belo > 0:
                                    chordMelody[chord_id][a - keyNum] += 1
                            a += 1
                        i += x
                        j += x
                    i = temp + 240

        self.__chordMelody += chordMelody

    def normalizeation(self, deleteList):
        deleteList = map(lambda n:n-1, deleteList)
        for i in range(0, len(self.__chordMelody)):
            sum = self.__chordMelody[i].sum()
            if sum == 0:
                sum = 1
            self.__chordMelody[i] = self.__chordMelody[i] / sum
        self.__chordMelody = np.delete(self.__chordMelody, deleteList, 0)

    def __replaceChord(self, keyNum, chord):
        i = 0
        chord_id = -1
        for item in self.__re_chord:
            if item.match(chord):
                j = 0
                for triad in self.__re_triad[i]:
                    if triad.match(chord):
                        chord_id = 1 + (12 + i - keyNum) % 12 * 5 + j
                    j += 1
                break
            i += 1

        return chord_id

    def __getKeyNum(self, key):
        if key.startswith('#'):
	    	return int(key[1:]) * 7 % 12
        else:
	    	return 12 - int(key[1:]) * 7 % 12

    def calcEmissionProbability(self, measure):
        emisson_probability = np.zeros(len(self.__chordMelody) + 2)
        i = 0
        for chord in self.__chordMelody:
            emisson_probability[i + 1] = np.dot(chord, measure)
            i += 1
        emisson_probability /= emisson_probability.sum()
#        for data in emisson_probability:
#            print data,
#        print ''
        return emisson_probability

    def getChordMelody(self):
        return self.__chordMelody

if __name__ == '__main__':
    melody = Melody('./song', './score')
    for chord in melody.getChordMelody():
        for x in chord:
            print x,
        print ''