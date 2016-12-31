# -*- coding:utf-8 -*-

import numpy as np
import os.path
import transition
import melody

class Analyze:
    def __init__(self, chordFolder, melodyFolder):
        #状態名
        self.states = [
            'start',
            'C', 'Cm', 'Caug', 'Cdim', 'Csus4',
            'C#', 'C#m', 'C#aug', 'C#dim', 'C#sus4',
            'D', 'Dm', 'Daug', 'Ddim', 'Dsus4',
            'D#', 'D#m', 'D#aug', 'D#dim', 'D#sus4',
            'E', 'Em', 'Eaug', 'Edim', 'Esus4',
            'F', 'Fm', 'Faug', 'Fdim', 'Fsus4',
            'F#', 'F#m', 'F#aug', 'F#dim', 'F#sus4',
            'G', 'Gm', 'Gaug', 'Gdim', 'Gsus4',
            'G#', 'G#m', 'G#aug', 'G#dim', 'G#sus4',
            'A', 'Am', 'Aaug', 'Adim', 'Asus4',
            'A#', 'A#m', 'A#aug', 'A#dim', 'A#sus4',
            'B', 'Bm', 'Baug', 'Bdim', 'Bsus4',
            'end']

        self.transition = transition.Transition(self.states)
        self.melody = melody.Melody(self.states)

        i = 1
        while True:
            chordFilename = chordFolder + '/' + str(i) + '.txt'
            if not os.path.exists(chordFilename):
                break
            melodyFilename = melodyFolder + '/' + str(i) + '.mid'
            if not os.path.exists(melodyFilename):
                break
            self.transition.analyze(chordFilename)
            self.melody.analyze(chordFilename, melodyFilename)
            i += 1
            
        deleteList = self.transition.getDeleteList()
        self.__new_states = self.transition.normalization(deleteList)
        self.melody.normalizeation(deleteList)

    def getNum(self):
        return len(self.__new_states)

    def getChord(self, id):
        return self.__new_states[id]

if __name__ == '__main__':
    transition = Transition('./song')
    for trans in transition.getTransitionProbability():
        for data in trans:
          print data,
        print ''