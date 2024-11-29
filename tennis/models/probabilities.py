'''
assume each point is i.i.d.
https://www.janmagnus.nl/papers/JRM065.pdf
'''
import numpy as np
import pandas as pd
import math

from scipy.stats import poisson
import matplotlib.pyplot as plt
from scipy.stats import poisson
import math

class Probabilities:

    def __init__(self):
        pass

        
    def expected_rank(self, atp_rank:int):
        """
        transform atp rank at start of match into expected rank 
        higher expected rank is better than lower: atp rank is opposite
        """
        return 8 - np.log(atp_rank)


    def prob_win_at_match_start(self, Ra, Rb):
        """
        Expected Rank of Player A
        Expected Rank of Player B
        const: mens singles: 0.0461, 0.3986, 0.0861; womens:0:7150
            prefer a higher constant to allocate a lower probability of a lower rank upset in certain circumstances of mens atp v womens wta
        """
        Dj = Ra - Rb
        return math.exp(0.0861 * Dj)  / (1 + math.exp(0.0861 * Dj)) 


    def prob_win_game(self, Pa):
        """[summary]
        Args:
            As ([type]): [description]
            Ar ([type]): [description]
            Bs ([type]): [description]
            Br ([type]): [description]
        """ 
        return (  Pa**4 * (-8*Pa**3+28*Pa**2-34*Pa+15)  ) / (  Pa**2 + (1-Pa)**2 )


    def win_point(self, ai, bi, ci, aav, di, ei):
        """
        Barnett & Clarke
            fi = expected percentage of points to win on serve for player i,
            gi = expected percentage of points to win on return for player i,

            ai = first serve percentage of player i,
            aav = average first serve percentage (across all players) [ plug for average opponent ],
            bi = first serve win percentage of player i
            ci = second serve win percentage of player i,
            di = first service return points win percentage of player i, and
            ei = second service return points win percentage of player i.
            """
        fi = ai * bi  + (1-ai) * ci
        gi = aav * di + (1-aav) * ei
        return fi, gi


    def win_point_avg_opp(self, ft, fi, fav, gj, gav):
        """
        ft = average percentage of points won on serve for tournament,
        fav = average percentage of points won on serve (across all players), and
        gav = average percentage of points won on return (across all players).
        """
        fij = ft +  (fi - fav) - (gj-gav)
        return fij


    # o'malley

    # def win_game():
    #     Gp = p**4 * (15- 4*p - (10*p**2)/ 1-2*p*(1-p))
    # def win_three_set_match():
    #     M3 = Set**2 * (1+ (2*(1-Set)))
    # def win_five_set_match():
    #     M5 = Set**3 * (1+ (3*(1-Set)) + (6(1-Set))**2)


    # def point_importance():
    # """ probability that player wins game if they win the point
    # """


    def prob_of_prop_occurance(self, k:int, mu:float, how:str=None):
        """  probability of prop bet occurance
        k: size
        mu: mean
        """
        def _poisson(mean, x):
            return mean**x * math.exp(-mean) / math.factorial(x)

        print(_poisson(x=k, mean=mu,))
        print(poisson.rvs(size=k, mu=mu))

        if how == 'eq':
            x = poisson.pmf(k=k, mu=mu)  # Probability Equal to Some Value
        elif how == 'lte':
            x = poisson.cdf(k=k, mu=mu) #Probability Less than Some Value
        elif how == 'gte':
            x = (1-poisson.cdf(k=k, mu=mu)) #Probability Greater than Some Value
        elif how == None:
            x = poisson.rvs(mu=mu, size=k)

        plt.hist(x, density=True, edgecolor='black')
        plt.show()


    # def prob_win_point():
    #     """
    #         probability that player wins point

    #         Ra  Rb (relative quality, gap between
    #         the two players)and Ra þ Rb (absolute quality,
    #         overall quality of the match)
    #         beta0 ; Constant (b0)0.6276 (0.0044)0.5486 (0.0051)
    #         beta1; Ranking difference (b1)0.0112 (0.0013)0.0212 (0.0015)
    #         beta2; Ranking sum (b2)0.0036 (0.0009)0.0022 (0.0010)

    #         Random effects
    #         Variance (s2)0.0026 (0.0002)0.0016 (0.0003)
    #         Correlation (c=s2) )0.4480 (0.0852) )0.6348 (0.2019)
    #     """
    #     XprimeA = (1, RankA-RankB, RankA + RankB)#XprimeA observed quality of player A against Player b
    #     Qa = XprimeA * BetaA + Na
    #     Yat = Qa + Eat # probability plaeyer A wins point t; Qa = Quality a; Eat Errors expected player a at time t
    #     # Q should include ranking as well as current form and or surface advantages
    #     Ybt = None# probability plaeyer B wins point t
    #     PaLessPb = 2(Beta0 = (Ra+Rb)*Beta2) 

    # def common_opponent():
    #     """
    #     spw
    #      In order to model how A and B would play against each
    #     other through their common opponents, Ci
    #     , we first need to calculate the differences in
    #     service points won by A and B against those opponents. Then we can additively combine
    #     those differences to come up with an indication of how well A would perform against B
    #     ∆ABi = (spw(A, Ci) − (1 − rpw(A, Ci))) − (spw(B, Ci) − (1 − rpw(B, Ci)))

    #     This value can be used to additively influence an arbitrary probability of winning a
    #     point on serve for player A or player B in any hierarchical model. Equation 16 shows how
    #     to estimate the probability of A beating B, given the results of matches of both players
    #     against Ci - M3(p, q) is the function described by O’Malley to calculate an estimate of
    #     the probability of winning a match.
    #     Pr(A beats B via Ci) ≈
    #     M3(0.6 + ∆AB
    #     i
    #     ,(1 − 0.6)) + M3(0.6,(1 − (0.6 − ∆AB
    #     i
    #     )))
    #     2

    #     spw(A, C i) - the percentage of service points won by A against C i.
    #     spw(B, C i) - the percentage of service points won by B against C i.
    #     rpw(A, C i) - the percentage of returning points won by A against C i.
    #     rpw(B, C i) - the percentage of returning points won by B against C i.

    #     take averages if faced common opponent multiplel times
    #     """
    #     deltaABi = spw(A, Ci) - (1 - rpw(A, Ci)) -  (spw(B, Ci)- (1- rpw(bi, Ci)))

    #     AbeatBviaC = (M3(0.6 + deltaABi, (1 - 0.6)) + M3(0.6, (1 - (0.6 - deltaABi)))) / 2

