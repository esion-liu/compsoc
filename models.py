"""
Voting Models
Definition of the ballots of the voters according to different generative models.
Results are probabilisty distributions over votes.
"""

import random
from pprint import pprint
import numpy as np
import scipy.stats as ss
import matplotlib.pylab as plt
from itertools import permutations, chain
from collections import Counter
from matplotlib.ticker import MaxNLocator
from utils import *

def generate_random_votes(number_voters, number_candidates):
    # Random generation of votes over candidates
    L = list(range(number_candidates))
    votes = []
    for vi in range(number_voters):
        random.seed()
        L = random.sample(L, number_candidates)
        votes.append(L)
    d = {}
    for v in votes:
        sv = int_list_to_str(v)
        d[sv] = (d[sv] + 1) if sv in d else 1
    ballots = []
    for k, v in d.items():
        kl = list(map(int, k.split(",")))
        ballots.append((v, kl))
    return ballots

def generate_gaussian_votes(mu, stdv, number_voters, number_candidates, plot_save=True):
    # Gaussian generation of votes over candidates
    V = list(permutations(range(number_candidates)))
    x = np.arange(-len(V)/2., len(V)/2.)
    xU, xL = x + mu, x - mu
    prob = ss.norm.cdf(xU, scale = stdv) - ss.norm.cdf(xL, scale = stdv) #scale specifies stdev
    prob /= prob.sum()
    dist = number_voters * prob
    dist = np.array(list(map(int, dist)))

    # Remove rankings with 0 occurence
    ballots = [(dist[i], list(V[i])) for i,_ in enumerate(x) if dist[i]]

    print ("> ", dist)
    print ("number_candidates = ", number_candidates)

    print ("ballots:\n", ballots)
    exit()


    if plot_save:
        fig, ax = plt.subplots()
        dist_non_null_index = np.array([i for i,x in enumerate(dist) if x])
        plt.plot(x[dist_non_null_index], dist[dist_non_null_index], 'b.-', lw=0.4)
        plt.grid(color='gray', linestyle='dashed', linewidth=0.1)
        plt.xticks(np.arange(min(x), max(x)+1, 1.0), rotation=90, fontsize=5)
        plt.xlabel("Votes")
        plt.ylabel("Number of occurences")
        ax.set_xticklabels(map(int_list_to_str, V))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title(r"{} voters, {} candidates, $\mu={}, \sigma={}$".format(number_voters, number_candidates, mu, stdv))
        plt.savefig('figures/Votes_gaussian_distrib.png', format='png', dpi=500)
    return ballots

def generate_multinomial_dirichlet_votes(alpha, num_voters, num_candidates):
    # Dirichlet Multinomial generation of votes over candidates
    candidates = list(range(1, num_candidates+1))
    P =  np.random.dirichlet(alpha, size = 1).tolist()[0]
    votes = []
    for i in range(num_voters):
        vote = np.random.choice(candidates, size=num_candidates, replace=False, p=P)
        vote = list(vote)
        votes.append(vote)
    ballots = []
    tmp = {}
    for vote in votes:
        vote_tuple = tuple(vote)
        if vote_tuple not in tmp:
            count = votes.count(vote)
            tmp[vote_tuple] = count
            ballots.append((count, list(vote_tuple)))
    return ballots

def test_gaussian():
    num_voters = 1000
    num_candidates = 4
    mu, stdv = 3, 10
    ballots = generate_gaussian_votes(mu, stdv, num_voters, num_candidates)
    pprint(ballots)

def test_dirichlet():
    num_voters = 20
    alpha_candidates = (1.1, 2.5, 3.8)
    num_candidates = len(alpha_candidates)
    ballots = generate_multinomial_dirichlet_votes(alpha_candidates, num_voters, num_candidates)
    pprint(ballots)

# test_gaussian()
# test_dirichlet()
