# BY: BP-2
# Contact: bp309420@ohio.edu or info@brady-phelps.dev

from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram
from IPython.display import display
from qiskit import *

from QuantumBracketsAlgorithms import controller, controller_matchup, controller_finals


# this program uses quantum probabilities (just hadamards) to predict march madness

# part of the point of this program is to track my progress within quantum computing, and to also use some
# statistical concepts I am learning in EE 3713.  I aim to rewrite this program next year using more advanced
# logic and concepts and hopefully make a smarter program. :)


# first is the round of 64 (16 matchups in 4 different regions)
# We are only going to use 1 qubit multiple times
qc = QuantumCircuit(1, 1)

# How do we determine probabilities?
# these are predetermined by historical data.

# 1 vs 16 = 0.74% chance of upset
# 2 vs 15 = 6.25% chance of upset
# 3 vs 14 = 15.3% chance of upset
# 4 vs 13 = 26.5% chance of upset
# 5 vs 12 = 35.4% chance of upset
# 6 vs 11 = 37.5% chance of upset
# 7 vs 10 = 39.6% chance of upset
# 8 vs 9 = 51.35% chance of upset (cool)

# Now we will implement these probabilities using some statistics

# First we create a 50% coin flip. This will correspond to 8 different states.
qc.h(0)

# This will be used to store winners
winner_round_64 = []
winner_round_32 = []
winner_round_16 = []
winner_round_8 = []
winner_round_4 = []

sim = AerSimulator()  # new sim for later

# Lets start with the 1 vs 16 seed
# to get a 0.74% chance using only 50% chances of 1's and 0's, lets

# we have a .78125% of getting a 1 7 times in a row.  (.5^7). **The Multiplication Rule for Independent Events**
# This is close enough to our actual probability, we can leave the rest up to basketball and quantum gods

# 8 matchups per region in this round (we start at index 1 because seed = 1)
num_round_64 = 9

# 4 matchups per region in round of 32
num_round_32 = 4

# 2 matchups per region in round of 16
num_round_16 = 2

# 1 matchup per region in elite 8
num_round_8 = 0

# final four and finals are an intersection between two or more regions so we do not have variables
# for them right now as they are special cases and the variables above are universal for all regions

# seed is used to determine which seed matchup we are currently doing
seed = 1
# take measurements
qc.measure(0, 0)
# display measurement
# display(qc.draw())

# loop through each 1 through 16 mathcups
while seed < num_round_64:
    region = 0
    num_matchups = 4
    # looping through all same seed matchup in each region
    while region < num_matchups:
        winner_round_64.append(controller(seed, qc))
        region += 1
    seed += 1
    
def star():
    print("*" * 100)
star()
print("WELCOME TO MY QUANTUM MARCH MADNESS PROGRAM!  PLEASE NOTE: USE THE RAW DATA FOR READING IN VALUES, THE FORMATTED output YOU CAN ALSO READ FROM BUT THE 1ST AND 4TH ROW SWAP AS WELL AS 2ND AND 3RD ROW SWAP EACH ITERATION. FOR RAW READING, READ LEFT TO RIGHT UNTIL YOU GET TO THE HALFWAY POINT.  THEN READ RIGHT TO LEFT STARTING FROM LAST VALUE.  (1,2,3,4,5,6,7,8 would be read 1,2,3,4,8,7,6,5). --THANK YOU, BP-2")
star()
# printing pretty
length = len(winner_round_64)-1
print("Round of 64 (raw): " + str(winner_round_64))
output = ""
region_counter = 1
for x in range(int(length/2)+1):
    output += str(winner_round_64[x]) + ", "
    if region_counter % 4 == 0:
        output += '\n'
    region_counter += 1
reverse = length
for x in range(int(length/2)+1):
    output += str(winner_round_64[reverse]) + ", "
    reverse -= 1
    if region_counter % 4 == 0:
        output += '\n'
    region_counter += 1
print("Round of 64: " + '\n' + output)

    

# now we do the round of 32, this means we will have 4 matchups per region between seeds determined from prior round
# this is where things get dicey, we cannot take the same approach that we did for the previous round because the permutations
# of matchups will scale exponentially with each round. 2^8 * 2^4 ...

# this is how I will approach the following rounds...


# I will assign each seed a weight

# I will have the weights 1-16 to sum up to 1.  This is so we can think of each weight easily as portion of 1

# WEIGHTS
# 136 possible points
# 1 - 16 points - 16/136 = 11.765
# 2 - 15 points - 15/136 = 11.03
# 3 - 14 points - 14/136 = 10.3
# 4 - 13 points - 13/136 = 9.56
# 5 - 12 points - 12/136 = 8.824
# 6 - 11 points - 11/136 = 8.1
# 7 - 10 points - 10/136 = 7.4
# 8 - 9 points - 9/136 = 6.6
# 9 - 8 points - 8/136 = 5.9
# 10 - 7 points - 7/136 = 5.1
# 11 - 6 points - 6/136 = 4.4
# 12 - 5 points - 5/136 = 3.7
# 13 - 4 points - 4/136 = 2.9
# 14 - 3 points - 3/136 = 2.2
# 15 - 2 points - 2/136 = 1.5
# 16 - 1 points - 1/136 = .7

# weights dictionary
weights = {
    1: 11.765,
    2: 11.03,
    3: 10.3,
    4: 9.56,
    5: 8.824,
    6: 8.1,
    7: 7.4,
    8: 6.6,
    9: 5.9,
    10: 5.1,
    11: 4.4,
    12: 3.7,
    13: 2.9,
    14: 2.2,
    15: 1.5,
    16: .7
}

star()

counter = 0
while counter < length:
    winner_round_32.append(controller_matchup(qc, winner_round_64[counter], winner_round_64[length], weights.get(
        winner_round_64[counter]), weights.get(winner_round_64[length])))
    counter += 1
    length -= 1
print("Round of 32 (raw): " + str(winner_round_32))

# printing pretty
length = len(winner_round_32)-1
output = ""
region_counter = 1
for x in range(int(length/2)+1):
    output += str(winner_round_32[x]) + ", "
    if region_counter % 4 == 0:
        output += '\n'
    region_counter += 1
reverse = length
for x in range(int(length/2)+1):
    output += str(winner_round_32[reverse]) + ", "
    reverse -= 1
    if region_counter % 4 == 0:
        output += '\n'
    region_counter += 1
print("Round of 32: " + '\n' + output)



counter = 0
while counter < length:
    winner_round_16.append(controller_matchup(qc, winner_round_32[counter], winner_round_32[length], weights.get(
        winner_round_32[counter]), weights.get(winner_round_32[length])))
    counter += 1
    length -= 1

star()

print("Sweet 16 (raw): " + str(winner_round_16))


# printing pretty
length = len(winner_round_16)-1
output = ""
region_counter = 1
for x in range(int(length/2)+1):
    output += str(winner_round_16[x]) + ", "
    if region_counter % 4 == 0:
        output += '\n'
    region_counter += 1
reverse = length
for x in range(int(length/2)+1):
    output += str(winner_round_16[reverse]) + ", "
    reverse -= 1
    if region_counter % 4 == 0:
        output += '\n'
    region_counter += 1
print("Sweet 16: " + '\n' + output)


counter = 0
while counter < length:
    winner_round_8.append(controller_matchup(qc, winner_round_16[counter], winner_round_16[length], weights.get(
        winner_round_16[counter]), weights.get(winner_round_16[length])))
    counter += 1
    length -= 1
star()
print("Elite 8 (raw): " + str(winner_round_8))
print("Elite 8: \n South: " + str(winner_round_8[0]) + "\n East: " + str(winner_round_8[1]) + "\n West: " + str(winner_round_8[2]) +" \n Midwest: " + str(winner_round_8[3]))



# now we need to mark each region because seed #'s could be same

# final four
winner_round_4.append(controller_finals(qc, winner_round_8[0], 1, winner_round_8[3], 4, weights.get(
    winner_round_8[0]), weights.get(winner_round_8[3])))
winner_round_4.append(controller_finals(qc, winner_round_8[1], 2, winner_round_8[2], 3, weights.get(
    winner_round_8[1]), weights.get(winner_round_8[2])))

star()

print("Final 4 (raw): " + str(winner_round_4[0]) + str(winner_round_4[1]))
output = "Final 4: \n"
match winner_round_4[0][1]:
    case(1):
        output += "South: " + str(winner_round_4[0][0]) + '\n'
    case(4):
        output += "Midwest: " + str(winner_round_4[0][0]) + '\n'
match winner_round_4[1][1]:
    case(2):
        output += "East: " + str(winner_round_4[1][0])
    case(3):
        output += "West: " + str(winner_round_4[1][0])
print(output)

star()

winner = controller_finals(qc, winner_round_4[0][0], winner_round_4[0][1], winner_round_4[1][0],
                           winner_round_4[1][1], weights.get(winner_round_4[0][0]), weights.get(winner_round_4[1][0]))
print("Winner is: " + str(winner))
output = ""
match winner[1]:
    case(1):
        output += "South: "
    case(2):
        output += "East: "
    case(3):
        output += "West: "
    case(4): 
        output += "Midwest: "
output += str(winner[0])
print (output)
star()