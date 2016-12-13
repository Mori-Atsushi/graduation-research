# -*- coding:utf-8 -*-

import numpy as np
import re
import pretty_midi

if __name__ == '__main__':
    chordFilename = './song/1.txt'
    midiFilename = './score/1.mid'
    midi_data = pretty_midi.PrettyMIDI(midiFilename)
    tempo = midi_data.get_tempo_changes()[1][0]
    chroma_data = midi_data.get_chroma(tempo)
    x = 7 * 240
    key = '#0'
    re_key = re.compile(r'^//[#b][0-9]$')
    re_rest = re.compile(r'^[0-9]+$')
    i = 0
    for line in open(chordFilename, 'r'):
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


#        print cellArray