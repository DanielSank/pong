from __future__ import division


def k(rating):
    """Totally arbitrary mobility function"""
    if rating < 100: return 40
    if rating < 200: return 20
    return 10


def elo(rating_a, rating_b, score_a, score_b, scale=100, base=10, k_func=k):
    """Compute new elo ratings from prior ratings and a game score.

    An elo rating describes the expected point spread in a game between two
    players. Each player has a weight Q. Given two players A and B with weights
    Q_A and Q_B, the expected fraction of points scored by player A is
        Q_A / (Q_A + Q_B).
    and similarly for B. This formulation has several important properties:
        1) For Q_A >> Q_B the expected fraction of points scored by A is 1.
        2) For Q_A << Q_B the expected fraction of points scored by A is 0.
        3) If Q_A == Q_B, the expected fraction of points scored by A is 1/2.
        4) The expected point fraction is self-normalized for any two Q values
            in the range [0, infinity).
        5) Multiplying all players' Q values by a constant leaves the expected
            points spread for any pair of players invariant.

    Because of properties 4 and 5, adding a new player N to an existing pool of
    players is always possible. Assuming we know that N's expected score
    fraction in games against the current best player B is x, then
        Q_N = Q_B * x / (1 - x).

    Being a single real number, these weights cannot capture un-orderable
    relations in players' relative skill. For example, if A always beats B, B
    always beats C, and C always beats A, then Q_A, Q_B, and Q_C are all equal.

    The elo rating is a logarithmic version of these weights, defined as
        rating = scale * log_base(Q).
    Therefore, if A's rating is N*scale larger than B's rating,
        rating_A = rating_B + N scale,
    then
        Q_A = base^N * Q_b
    and A's expected point fraction in games against B is
        base^N / (1 + base^N).

    So far we have defined what weights and elo ratings mean, but we have not
    discussed how to recalculate them as new information comes in, i.e. as new
    games are played. In fact, the elo system refers to both the rank itself and
    the update system. Given the score of a new game, we compute a player's
    point actual scored point fraction S, and incriment that player's rank by
        k (S - E)
    where E is that player's expected point fraction for the game and k is a
    a value describing our willingness to update that player's rank. k could be
    a constant, a function of the player's rating prior to the game, or even a
    function of the entire history of the scoring system.

    Todo: Understand why the increment in the rating (as opposed to the weight)
        is proportial to the error using real statistics. Assume that on each
        point, the probability that A wins the point is P_A = Q_A / (Q_A + Q_B).
        Then we have two simultaneous random walk processes with absorbing
        boundary conditions and correlated statistics. Not sure how to treat
        that yet :-\

    Args:
        rating_a, rating_b (float): The two players' ratings before the game
            was played.
        score_a, score_b (int): The players' scores.
        scale (float): scale used for this rating system.
        k_func (function): Takes a player's pre-game rank (a float) and returns
            a float. More sophisticated k functions could be used in princple.

    Returns (tuple(float, float)):
        New ratings for the two players.
    """
    Q_a = base**(rating_a / scale)
    Q_b = base**(rating_b / scale)
    # Pre-game weights

    E_a = Q_a / (Q_a + Q_b)
    E_b = Q_b / (Q_a + Q_b)
    # Expected fraction of points scored by each player.

    norm_score_a = score_a / (score_a + score_b)
    norm_score_b = score_b / (score_a + score_b)
    # Actual fraction of points scored by each player.

    k_a = k_func(rating_a)
    k_b = k_func(rating_b)
    # Score mobilities.

    new_rating_a = rating_a + k_a * (norm_score_a - E_a)
    new_rating_b = rating_b + k_b * (norm_score_b - E_b)

    return new_rating_a, new_rating_b

