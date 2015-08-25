from __future__ import division

def k(rating):
    if rating < 100: return 40
    if rating < 200: return 20
    return 10

def elo(rating_a, rating_b, score_a, score_b, scale=100, k_func=k):

    Q_a = 10**(rating_a / scale)
    Q_b = 10**(rating_b / scale)
    E_a = Q_a / (Q_a + Q_b)
    E_b = Q_b / (Q_a + Q_b)

    k_a = k_func(rating_a)
    k_b = k_func(rating_b)

    norm_score_a = score_a / (score_a + score_b)
    norm_score_b = score_b / (score_a + score_b)

    new_rating_a = rating_a + k_a * (norm_score_a - E_a)
    new_rating_b = rating_b + k_b * (norm_score_b - E_b)

    return new_rating_a, new_rating_b

