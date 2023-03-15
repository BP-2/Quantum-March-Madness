# BY: BP-2
# Contact: bp309420@ohio.edu or info@brady-phelps.dev
# The following file contains algorithms used by the QuantumBrackets.py program.  This is largely for calculating probabilities
# of each matchup.


import random
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram
from IPython.display import display
from qiskit import *


sim = AerSimulator()  # new sim for later


# we have a .78125% of getting a 1 7 times in a row.  (.5^7). **The Multiplication Rule for Independent Events**
# This is close enough to our actual probability, we can leave the rest up to basketball and quantum gods
def one_sixteen(qc):
    # use local simulator
    # 7 shots, if they are all 1, we will consider this an upset!
    result = execute(qc, backend=sim, shots=7).result()
    counts = result.get_counts()
    if counts.get('1') == 7:
        # print("Upset") debug
        return 16
    else:
        return 1

# we have a 6.25% of getting a 1 4 times in a row.  (.5^4). **The Multiplication Rule for Independent Events**


def two_fifteen(qc):
    # 4 shots, if they are all 1, we will consider this an upset!
    result = execute(qc, backend=sim, shots=4).result()
    counts = result.get_counts()
    if counts.get('1') == 4:
        # print("Upset") debug
        return 15
    else:
        return 2

# we can have a 15.625% chance if we multiply the probability of getting a 1 five times in a row times five
# this is Multiplication Rule for Independent events (AND) as well as adding independent events (OR)


def three_fourteen(qc):
    results = []
    # trial 5 seperate times (OR)
    while len(results) < 5:
        results.append(
            execute(qc, backend=sim, shots=5).result().get_counts())  # 5 shots

    for x in results:
        if x.get('1') == 5:
            # print("Upset") debug
            return 14
        else:
            return 3
# we have a 25% of getting a 1 2 times in a row.  (.5^3). **The Multiplication Rule for Independent Events**


def four_thirteen(qc):
    # 2 shots, if they are all 1, we will consider this an upset!
    result = execute(qc, backend=sim, shots=2).result()
    counts = result.get_counts()
    if counts.get('1') == 2:
        # print("Upset") debug
        return 13
    # adding this on to reach 26.56%, this is because this is closer to actual probability
    # we know this is true because we can see 25% + .78125% + .78125% = 26.56%
    elif one_sixteen(qc) == 16 or one_sixteen(qc) == 16:
        # print("Upset") debug
        return 13
    else:
        return 4
# we are now going to combine some of our other functions to speed up the calculation process
# we can get 32.81% by doing four_thirteen (26.56%) + two_fifteen (6.25%)
# then we can add the probability of getting five ones in a row (3.125%), and get 35.935% (close enough)


def five_twelve(qc):
    if four_thirteen(qc) == 13 or two_fifteen(qc) == 15:
        # print("Upset") debug
        return 12
    # 5 shots, if they are all 1, we will consider this an upset!
    result = execute(qc, backend=sim, shots=5).result()
    counts = result.get_counts()
    if counts.get('1') == 5:
        # print("Upset") debug
        return 12
    return 5

# here we add independent events five_twelve (35.935%) with one_sixteen (.78125%) and another one_sixteen (.78125%) = 37.4975%


def six_eleven(qc):
    if five_twelve(qc) == 12 or one_sixteen(qc) == 16 or one_sixteen(qc) == 16:
        # print("Upset") debug
        return 11
    return 6
# 26.56% + 6.25% + .78125% = 39.84125


def seven_ten(qc):
    if four_thirteen(qc) == 13 or two_fifteen(qc) == 15 or one_sixteen(qc) == 16:
        # print("Upset") debug
        return 10
    return 7
# for this we have 50% + .78125% to put the probability at 50.78125%


def eight_nine(qc):
    # 1 shots, if 1, we will consider this an upset!
    result = execute(qc, backend=sim, shots=1).result()
    counts = result.get_counts()
    if counts.get('1') == 1 or one_sixteen(qc) == 16:
        # print("Upset") debug
        return 9
    return 8

# this controller controlls the flow of the program for round of 64


def controller(seed, qc):
    match (seed):
        case(1):
            return one_sixteen(qc)
        case(2):
            return two_fifteen(qc)
        case(3):
            return three_fourteen(qc)
        case(4):
            return four_thirteen(qc)
        case(5):
            return five_twelve(qc)
        case(6):
            return six_eleven(qc)
        case(7):
            return seven_ten(qc)
        case(8):
            return eight_nine(qc)
        case _:
            return 0

# this controller controls flow of program for rounds 32-8
def controller_matchup(qc, seed, seed_two, weight, weight_two):
    total = weight + weight_two
    # the probability that the underdog wins is weight_two / total
    probability = weight_two/total

    # at this point we can not longer do the old method of modeling probabilities with quantum gates
    # because I would have to write something for all cases.  I could simply use classical computing
    # to get the exact probability using my previous weighting, however, that loses some of the
    # quantum magic.  So, I will be combining my classical weighting with some quantum variability.
    # I will be doing this by applying a hadamard before each calculating (done in main), and if it is a 1,
    # the underdog will get a boost (3%), if it is a 0 the favorite will get a boost (1.5%)

    result = execute(qc, backend=sim, shots=1).result()
    counts = result.get_counts()
    if counts.get('1') == 1 and weight_two < weight:  # underdog & quantum choice
        probability += .03
    elif counts.get('1') == 1:  # favorite and quantum choice
        probability += .015
    elif weight_two < weight:  # underdog and not quantum choice
        probability -= .015
    else:  # favorite and not quantum choice
        probability -= .03
    # this will return a random decimal value between 0 and 1
    if random.random() <= probability:
        # print(probability) debug
        return seed_two
    return seed

# have to add indexes for the finals due to duplicate seed values
def controller_finals(qc, seed, index, seed_two, index_two, weight, weight_two):
    total = weight + weight_two
    # the probability that the underdog wins is weight_two / total
    probability = weight_two/total

    # at this point we can not longer do the old method of modeling probabilities with quantum gates
    # because I would have to write something for all cases.  I could simply use classical computing
    # to get the exact probability using my previous weighting, however, that loses some of the
    # quantum magic.  So, I will be combining my classical weighting with some quantum variability.
    # I will be doing this by applying a hadamard before each calculating (done in main), and if it is a 1,
    # the underdog will get a boost (3%), if it is a 0 the favorite will get a boost (1.5%)

    result = execute(qc, backend=sim, shots=1).result()
    counts = result.get_counts()
    if counts.get('1') == 1 and weight_two < weight:  # underdog & quantum choice
        probability += .03
    elif counts.get('1') == 1:  # favorite and quantum choice
        probability += .015
    elif weight_two < weight:  # underdog and not quantum choice
        probability -= .015
    else:  # favorite and not quantum choice
        probability -= .03
    # this will return a random decimal value between 0 and 1
    if random.random() <= probability:
        # print(probability) debug
        return [seed_two, index_two]
    return [seed, index]
