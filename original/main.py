# -*- coding:utf-8 -*-

import numpy as np
from hmmlearn import hmm
import chord
import midi
import melody

if __name__ == '__main__':
    filename = 'test.mid'
    chordFolder = './chord'
    melodyFolder = './melody'

    songMidi = midi.Midi(filename)
    phrase = songMidi.getPhrase()
    transition = chord.Analyze(chordFolder, melodyFolder)
    n_states = transition.getNum()
    model = hmm.MultinomialHMM(n_components = n_states)

    #初期状態確率の定義
    start_probability = np.zeros(n_states)
    start_probability[0] = 1
    model.startprob_ = start_probability

    #遷移確率の定義
    model.transmat_ = transition.transition.getTransitionProbability()
#    for trans in model.transmat_:
#        for data in trans:
#          print data,
#        print ''

    #出力確率の定義
    emission_probability = np.empty((n_states, 0))
    temp = np.zeros(n_states)
    temp[0] = 1.0
    emission_probability = np.c_[emission_probability, temp]
    i = 1
    for measure in phrase:
        temp = transition.melody.calcEmissionProbability(measure)
        emission_probability = np.c_[emission_probability, temp]
        i += 1
    temp = np.zeros(n_states)
    for i in range(n_states):
        if transition.getChord(i)[1] == 'end':
            temp[i] = 1.0
    emission_probability = np.c_[emission_probability, temp]
    model.emissionprob_ = emission_probability

    test = np.matrix(np.arange(len(phrase) + 2)).T
    result = model.predict(test)
    for item in result:
        print transition.getChord(item),