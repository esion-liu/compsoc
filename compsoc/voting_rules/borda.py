"""
Computes the Borda score for a candidate.
"""
from compsoc.profile import Profile

def borda_rule(profile: Profile, candidate: int) -> int:
    """
    Calculates the Borda score for a candidate based on a profile.

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The Borda score for the candidate.
    :rtype: int
    """
    # Max score to be applied with borda count
    top_score = len(profile.candidates) - 1

    # Get pairwise scores
    scores = [pair[0] * (top_score - pair[1].index(candidate)) for
              pair in profile.pairs]

    # Return the total score
    return sum(scores)
