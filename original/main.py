# -*- coding:utf-8 -*-

import numpy as np
from hmmlearn import hmm
import pretty_midi

class Song:
    def __init__(self, filename):
        midi_data = pretty_midi.PrettyMIDI(filename)
        tempo = midi_data.get_tempo_changes()[1][0]
        chroma_data = midi_data.get_chroma(tempo)
        self.__melody_data = np.zeros((len(chroma_data[0]) / 240 + 1, 12))
        i = 0
        for data in chroma_data:
            j = 0
            for belo in data:
                if belo > 0:
                    self.__melody_data[j / 240][i] += 1
                j += 1
            i += 1
        print self.__melody_data

if __name__ == '__main__':
    song = Song('test.mid')