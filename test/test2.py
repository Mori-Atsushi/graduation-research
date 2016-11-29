# -*- coding:utf-8 -*-

import numpy as np
from hmmlearn import hmm

if __name__ == '__main__':
    states = ["Start", "Rainy", "Sunny", "Finish"]
    n_states = len(states)

    observations = ["start", "walk", "shop", "clean", "finish"]
    n_observations = len(observations)

    start_probability = np.array([1.0, 0, 0, 0])

    transition_probability = np.array([
        [0, 0.6, 0.4, 0],
        [0, 0.6, 0.2, 0.2],
        [0, 0.3, 0.5, 0.2],
        [0, 0, 0, 1]
    ])

    emission_probability = np.array([
        [1, 0, 0, 0, 0],
        [0, 0.1, 0.4, 0.5, 0],
        [0, 0.6, 0.3, 0.1, 0],
        [0, 0, 0, 0, 1]
    ])

    model = hmm.MultinomialHMM(n_components = n_states)
    model.startprob_ = start_probability
    model.transmat_ = transition_probability
    model.emissionprob_ = emission_probability

    # predict a sequence of hidden states based on visible states
    bob_says = np.array([[0, 1, 3, 2, 2, 3, 1, 4]]).T

#    model = model.fit(bob_says)
    logprob, alice_hears = model.decode(bob_says, algorithm="viterbi")
    print("Bob says:", ", ".join(map(lambda x: observations[x], bob_says)))
    print("Alice hears:", ", ".join(map(lambda x: states[x], alice_hears)))