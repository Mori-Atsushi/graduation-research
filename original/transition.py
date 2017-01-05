# -*- coding:utf-8 -*-

import numpy as np
import re

class Transition:
    def __init__(self, states):
        self.__states = states
        self.__n_states = len(states)
        self.__transition = np.zeros((self.__n_states, self.__n_states))
        self.__transition[-1][-1] = 1
        self.__re_key = re.compile(r'^//[#b][0-9]$')
        self.__re_rest = re.compile(r'^[0-9]+$')
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

    def analyze(self, filename):
        chordList = []
        key = '#0'
        for line in open(filename, 'r'):
            if line.startswith('//'):
                if self.__re_key.match(line):
                    key = line[2:]
                continue
            cellArray = line.split('|')
            cellArray.pop()
            for cell in cellArray:
                if self.__re_rest.match(cell):
                    chordList.append(-1)
                else:
                    chordArray = cell.split(' ')
                    lastChord = -1
                    for chord in chordArray:
                        if lastChord != chord:
                            chordList.append(self.__replaceChord(key, chord))
                            lastChord = chord
        chordList.append(-1)

        endChord = 61
        lastChord = [0, 0]
        for chord in chordList:
            if chord == -1:
                chord = endChord
            if (lastChord[0] == 0 and lastChord[1] == 0) and chord == endChord:
                continue
            self.__transition[lastChord[0] * 62 + lastChord[1]][lastChord[1] * 62 + chord] += 1
            if chord == endChord:
                lastChord[0] = 0
                lastChord[1] = 0
            else:
                lastChord[0] = lastChord[1]
                lastChord[1] = chord

    def normalization(self, deleteList):
        appendList = []
        for i in range(len(self.__transition)):
            sum = self.__transition[i].sum()
            if sum == 0:
                self.__transition[i][len(self.__transition[i]) - 1] = 1
                sum = 1
            self.__transition[i] = self.__transition[i] / sum
        self.__transition = np.delete(self.__transition, deleteList, 0)
        self.__transition = np.delete(self.__transition, deleteList, 1)
        new_states = []
        i = 0
        for data in range(len(self.__states)):
            if data == deleteList[i]:
                if i < len(deleteList) - 1:
                    i += 1
            else:
                new_states.append(self.__states[data])
        return new_states

    def __replaceChord(self, key, chord):
        if key.startswith('#'):
	    	keyNum = int(key[1:]) * 7 % 12
        else:
	    	keyNum = 12 - int(key[1:]) * 7 % 12

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

    def getTransitionProbability(self):
        return self.__transition

    def getDeleteList(self):
        deleteList = []
        row_sum = np.sum(self.__transition, axis=0)
        col_sum = np.sum(self.__transition, axis=1)
        for i in range(len(self.__transition)):
            if row_sum[i] == 0 and col_sum[i] == 0:
                deleteList.append(i)
        return deleteList