# -*- coding:utf-8 -*-

import numpy as np
import pretty_midi

class Midi:
    def __init__(self, filename):
        self.__midi_data = pretty_midi.PrettyMIDI(filename)

    def getPhrase(self):
        tempo = self.__midi_data.get_tempo_changes()[1][0]
        chroma_data = self.__midi_data.get_chroma(tempo)
        melody_data = np.zeros((len(chroma_data[0]) / 240 + 1, 12))
        i = 0
        for data in chroma_data:
            j = 0
            for belo in data:
                if belo > 0:
                    melody_data[j / 240][i] += 1
                j += 1
            i += 1
        return melody_data

if __name__ == '__main__':
    midi = Midi('test.mid')
    print midi.getPhrase()