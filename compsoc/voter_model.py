"""
Voter models
Definition of the ballots of the voters according to different generative models.
Results are probabilistic distributions over votes.
"""

import random
from collections import Counter
from itertools import permutations
from typing import List, Optional, Tuple

import matplotlib.pylab as plt
import numpy as np
import scipy.stats as ss
from matplotlib.ticker import MaxNLocator

from compsoc.profile import Profile
from compsoc.utils import int_list_to_str


def generate_random_votes(number_voters: int,
                          number_candidates: int) -> List[Tuple[int, Tuple[int, ...]]]:
    candidate_list = list(range(number_candidates))
    votes = [random.sample(candidate_list, number_candidates) for _ in range(number_voters)]
    vote_strs = [int_list_to_str(vote) for vote in votes]
    vote_counts = Counter(vote_strs)
    ballots = [(count, tuple(map(int, vote.split(',')))) for vote, count in vote_counts.items()]
    return ballots


def generate_gaussian_votes(mu: float,
                            stdv: float,
                            num_voters: int,
                            num_candidates: int,
                            plot_save: Optional[bool] = True) -> List[Tuple[int, Tuple[int, ...]]]:
    # Gaussian generation of votes over candidates
    ballot_permutations = list(permutations(range(num_candidates)))
    x = np.arange(-len(ballot_permutations) / 2., len(ballot_permutations) / 2.)
    x_u, x_l = x + mu, x - mu
    prob = ss.norm.cdf(x_u, scale=stdv) - ss.norm.cdf(x_l, scale=stdv)  # scale specifies stdev
    prob /= prob.sum()
    dist = num_voters * prob
    dist = np.array(list(map(int, dist)))

    # Adjust the number of voters to match the desired number of voters
    total_voters = dist.sum()
    diff = num_voters - total_voters
    if diff != 0:
        max_index = np.argmax(dist)
        dist[max_index] += diff

    # Remove rankings with 0 occurence
    ballots = [(int(dist[i]), tuple(ballot_permutations[i])) for i, _ in enumerate(x) if dist[i]]
    if plot_save:
        _, ax = plt.subplots()
        dist_non_null_index = np.array([i for i, x in enumerate(dist) if x])
        plt.plot(x[dist_non_null_index], dist[dist_non_null_index], 'b.-', lw=0.4)
        plt.grid(color='gray', linestyle='dashed', linewidth=0.1)
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0), rotation=90, fontsize=5)
        plt.xlabel('Votes')
        plt.ylabel('Number of occurences')
        ax.set_xticklabels(map(int_list_to_str, ballot_permutations))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title(rf'{num_voters} voters, {num_candidates} candidates, $\mu={mu}, $\sigma={stdv}$')
        plt.savefig('figures/Votes_gaussian_distribution.png', format='png', dpi=500)
    return ballots


def generate_multinomial_dirichlet_votes(alpha: Tuple[float, ...],
                                         num_voters: int,
                                         num_candidates: int) -> List[Tuple[int, Tuple[int, ...]]]:
    """
    Generates a list of pairs (count, vote) from a Dirichlet Multinomia model of voters.
    """
    if len(alpha) != num_candidates:
        raise ValueError(f"Alpha should have {num_candidates} values, but has {len(alpha)}")
    candidates = list(range(num_candidates))
    p = np.random.dirichlet(alpha, size=1).tolist()[0]
    votes = [tuple(np.random.choice(candidates, size=num_candidates, replace=False, p=p))
             for _ in range(num_voters)]
    vote_counts = Counter(votes)
    ballots = [(count, vote) for vote, count in vote_counts.items()]
    return ballots


def get_profile_from_model(num_candidates: int, num_voters: int, voters_model: str,
                           verbose=False) -> Profile:
    """
    Generates a profile from a model of voters.
    """
    pairs = get_pairs_from_model(num_candidates, num_voters, voters_model)
    profile = Profile(pairs)

    if verbose:
        print(profile)

    return profile


def get_pairs_from_model(num_candidates: int, num_voters: int, voters_model: str):
    """
    Generates a list of pairs (count, vote) from a model of voters.
    """
    if voters_model == "multinomial_dirichlet":
        # The population hyperparam should be set according the competition goals.
        # alpha = (1.1, 2.5, 3.8, 2.1, 1.3)
        # Random alphas might cause precision problems with the generation of P, when values are
        # small
        alpha = tuple(np.random.rand(1, num_candidates)[0])
        pairs = generate_multinomial_dirichlet_votes(alpha, num_voters, num_candidates)
    elif voters_model == "gaussian":
        mu, stdv = 2, 1  # Depends on 'num_voters'
        pairs = generate_gaussian_votes(mu, stdv, num_voters, num_candidates)
    elif voters_model == "random":
        pairs = generate_random_votes(num_voters, num_candidates)
    else:
        pairs = generate_random_votes(num_voters, num_candidates)
    return pairs
