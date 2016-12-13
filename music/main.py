# -*- coding:utf-8 -*-

import numpy as np
from hmmlearn import hmm
import chord
import melody
import midi

class States:
    def __init__(self, phrase):
        songFolder = './song'
        scoreFolder = './song'
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
        
        #状態数
        self.__n_states = len(self.states)

        #初期状態確率の定義
        self.__start_probability = np.zeros(self.__n_states)
        self.__start_probability[0] = 1

        #遷移確率の定義
        transition = chord.Transition(songFolder)
        self.__transition_probability = transition.getTransitionProbability()

        #出力確率の定義
        self.__emission_probability = np.empty((self.__n_states, 0))
        temp = np.zeros(self.__n_states)
        temp[0] = 1.0
        self.__emission_probability = np.c_[self.__emission_probability, temp]
        melo = melody.Melody(songFolder, scoreFolder)
        i = 1
        for measure in phrase:
            temp = melo.calcEmissionProbability(measure)
            self.__emission_probability = np.c_[self.__emission_probability, temp]
            i += 1
        temp = np.zeros(self.__n_states)
        temp[-1] = 1.0
        self.__emission_probability = np.c_[self.__emission_probability, temp]

    #状態数の取得
    def getNum(self):
        return self.__n_states
    
    #初期状態確率
    def getStartProbability(self):
        return self.__start_probability

    #遷移確率
    def getTransitionProbability(self):
        return self.__transition_probability

    #出力確率
    def getEmissonProbability(self):
        return self.__emission_probability


if __name__ == '__main__':
    midi = midi.Midi('test.mid')
    phrase = midi.getPhrase()

    states = States(phrase)
    model = hmm.MultinomialHMM(n_components = states.getNum())
    model.startprob_ = states.getStartProbability()
    model.transmat_ = states.getTransitionProbability()
    model.emissionprob_ = states.getEmissonProbability()

    test = np.matrix(np.arange(len(phrase) + 2)).T
    result = model.predict(test)
    for item in result:
        print states.states[item],