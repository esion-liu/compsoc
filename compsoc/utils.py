from profile import Profile
from typing import Tuple, Set
from collections import Counter
import random

"""
This module contains utility functions for the compsoc website.
"""


# int-str converters
def int_list_to_str(int_list: list[int]) -> str:
    """
    Converts a list of integers to a comma-separated string.

    :param int_list: A list of integers.
    :type int_list: list[int]
    :return: A comma-separated string.
    :rtype: str
    """
    return ','.join(map(str, int_list))


def str_list_to_in(str_list: str) -> list[int]:
    """
    Converts a comma-separated string to a list of integers.

    :param str_list: A comma-separated string.
    :type str_list: str
    :return: A list of integers.
    :rtype: list[int]
    """
    return list(map(int, str_list.split(',')))

# create distorted profiles
def distort_profile(origin_profile: Profile, distort_rate: float) -> Set[Tuple[int, Tuple[int, ...]]]:
    """
    Convert a complete profile to a set of distorted ballots
    :param origin_profile: the Profile to be distorted
    :type origin_profile: Profile
    :param distort_rate: the percentage to remain
    :type distort_rate: float (between 0 and 1)
    return: a set to represent ballots
    :rtype: Set[Tuple[int, Tuple[int, ...]]]
    """

    ballots = [[item[0], list(item[1])] for item in origin_profile.pairs]

    total_ranking = 0
    for i in ballots:
        total_ranking += i[0]*len(i[1])
    num_to_remove = round(total_ranking * (1.0 - distort_rate))

    ballots = [[elem[1]] * elem[0] for elem in ballots]
    ballots = [item for sublist in ballots for item in sublist]
    temp = []
    for i in range(len(ballots)):
        temp.append(ballots[i][:])
    ballots = temp

    flag = False
    for _ in range(num_to_remove):
        to_remove = random.randint(0, len(ballots) - 1)
        tol = 100
        while len(ballots[to_remove]) == 2:
            to_remove = random.randint(0, len(ballots) - 1)
            tol -= 1
            if tol == 0:
                flag = True
                break
        if flag:
            break
        ballots[to_remove].pop(random.randint(0, len(ballots[to_remove]) - 1))

    counter = Counter(map(tuple, ballots))
    result = set()
    for item, count in counter.items():
        result.add((count,item))

    return result
        
        

    
        



