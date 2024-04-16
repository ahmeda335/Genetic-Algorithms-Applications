# -------------------------------------------- #
# ----------- Sudoko-Problem ----------------- #
# -------------------------------------------- #

# - This code is a Genetic Algorithms code to solve sudoko problem, but it
# rarely solvs it, as it often gets to a local optima.
# - You can change the parameters or the methods used in GA operators "selection,
# mutation and crossover ) to get a better and nearer results to the problem.

import numpy as np
from copy import deepcopy
import time

INPUT_MATRAX = []

def taking_input():
    """
    This function takes the input sudoko matrix to be solved from the user.
    :return: the taken matrix.
    """
    global INPUT_MATRAX
    INPUT_MATRAX = [[int(input()) for x in range(9)] for y in range(9)]  # 9
    return


def creating_chromosome(pre_chromosome):
    """
    - Genetic Algorithm depends mainly on creating a random solution (chromosome),
    then improving it. The shape of this chromosome depends on the problem.
    :param pre_chromosome: the input matrix from the user.
    :return: one chromosome (random solution)
    """

    # - The user enters the sudoko matrix such that he puts the fixed number and the nonfound numbers
    # are put zeros.
    # - Then I initialize initial solutions such that in each subgrid 3x3 matrix there is no repeated
    # numbers by keeping the fixed number at its poitions, then improving the solution by improving the
    # laws and columns.

    chromosome = pre_chromosome
    for i in range(9):  # 9
        for j in range(9):
            if (i < 3) and (j < 3):
                if chromosome[i][j] == 0:
                    rand_num = np.random.randint(1, 10)  # 10 not included
                    while rand_num in (chromosome[0][:3] + chromosome[1][:3] + chromosome[2][:3]):
                        rand_num = np.random.randint(1, 10)
                    chromosome[i][j] = rand_num
            elif i < 3 and 6 > j >= 3:
                if chromosome[i][j] == 0:
                    rand_num = np.random.randint(1, 10)
                    while rand_num in (chromosome[0][3:6] + chromosome[1][3:6] + chromosome[2][3:6]):
                        rand_num = np.random.randint(1, 10)
                    chromosome[i][j] = rand_num
            elif i < 3 and 9 > j >= 6:
                if chromosome[i][j] == 0:
                    rand_num = np.random.randint(1, 10)
                    while rand_num in (chromosome[0][6:9] + chromosome[1][6:9] + chromosome[2][6:9]):
                        rand_num = np.random.randint(1, 10)
                    chromosome[i][j] = rand_num
            elif 6 > i >= 3 and j < 3:
                if chromosome[i][j] == 0:
                    rand_num = np.random.randint(1, 10)
                    while rand_num in (chromosome[3][:3] + chromosome[4][:3] + chromosome[5][:3]):
                        rand_num = np.random.randint(1, 10)
                    chromosome[i][j] = rand_num
            elif 6 > i >= 3 and 6 > j >= 3:
                if chromosome[i][j] == 0:
                    rand_num = np.random.randint(1, 9)
                    while rand_num in (chromosome[3][3:6] + chromosome[4][3:6] + chromosome[5][3:6]):
                        rand_num = np.random.randint(1, 10)
                    chromosome[i][j] = rand_num
            elif 6 > i >= 3 and 9 > j >= 6:
                if chromosome[i][j] == 0:
                    rand_num = np.random.randint(1, 10)
                    while rand_num in (chromosome[3][6:9] + chromosome[4][6:9] + chromosome[5][6:9]):
                        rand_num = np.random.randint(1, 10)
                    chromosome[i][j] = rand_num
            elif 9 > i >= 6 and j < 3:
                if chromosome[i][j] == 0:
                    rand_num = np.random.randint(1, 10)
                    while rand_num in (chromosome[6][:3] + chromosome[7][:3] + chromosome[8][:3]):
                        rand_num = np.random.randint(1, 10)
                    chromosome[i][j] = rand_num
            elif 9 > i >= 6 and 6 > j >= 3:
                if chromosome[i][j] == 0:
                    rand_num = np.random.randint(1, 10)
                    while rand_num in (chromosome[6][3:6] + chromosome[7][3:6] + chromosome[8][3:6]):
                        rand_num = np.random.randint(1, 10)
                    chromosome[i][j] = rand_num
            elif 9 > i >= 6 and 9 > j >= 6:
                if chromosome[i][j] == 0:
                    rand_num = np.random.randint(1, 10)
                    while rand_num in (chromosome[6][6:9] + chromosome[7][6:9] + chromosome[8][6:9]):
                        rand_num = np.random.randint(1, 10)
                    chromosome[i][j] = rand_num
    return chromosome


def fitness(chromosome):
    """
    - This is the fitness funciton I will detect the good solutions from the bad ones.
    - In this case I detected number of repeated numbers in rows and columns.
    :param chromosome: One solution from the population.
    :return: the fitness of the solution.
    """
    fitness = 0
    for i in range(len(chromosome)):
        fitness += len(chromosome[i]) - len(set(chromosome[i]))
        vertical_lst = []
        for j in range(len(chromosome)):
            vertical_lst.append(chromosome[j][i])
        fitness += len(vertical_lst) - len(set(vertical_lst))

    return fitness


def making_population(pop_size):
    """
    - Creating lots of chromosomes (of course, I won't make only one random solution -chromosome-)
    to improve them.
    :param pop_size: Number of chromosomes (random solutions) I want to initialize.
    :return: the population.
    """
    global INPUT_MATRAX
    taking_input()
    population = []
    for i in range(pop_size):
        chromosome = creating_chromosome(deepcopy(INPUT_MATRAX))
        population.append(chromosome)
    return population


def sorting(population):
    """
    - Sorting the chromosomes according to their fitness.
    :param population: the population of chromosomes (random solutions)
    :return: the sorted population.
    """
    population = sorted(population, key=fitness)
    return population


def crossover(population, a, b, pc):
    """
    - The second step in GA. I generate new offstring (children) from current solutions (parents).
    There are many methods to do that depending on the problem.
    :param population: the population of the solutions.
    :param a: random solution (parent1).
    :param b: another random solution (parent2)
    :param pc: probability of crossover, I use to minimize the probability of the crossover. I can change it.
    :return: the new offspring.
    """
    parent1 = a
    parent2 = b
    pc = pc

    if np.random.rand() < pc:
        child1 = parent1[:6] + parent2[6:]
        child2 = parent2[:3] + parent1[3:6] + parent1[6:]
    else:
        child1 = parent1
        child2 = parent2
    population.append(child1)
    population.append(child2)

    return population


def random_mutation(cromosome, pc):
    """
    - This is the third and last step in GA. I make some changes in the sudoko matrix,
    but take care of the rules and the fixed places.
    - These line of codes changes depending on the sudoko matrix.
    :param cromosome:
    :param pc:
    :return:
    """
    cromosome = cromosome
    pc = pc
    if np.random.rand() < pc:
        # These swaps changes each time I solve a different sudoko matrix.
        # The Sudoko matrix is specialized for is at the end of the program.
        # TODO: I can't handle to make random swaps
        cromosome[0][1], cromosome[2][0] = cromosome[2][0], cromosome[0][1]
        cromosome[1][3], cromosome[0][5] = cromosome[0][5], cromosome[1][3]
        cromosome[0][1], cromosome[2][2] = cromosome[2][2], cromosome[0][1]
        cromosome[8][8], cromosome[6][7] = cromosome[6][7], cromosome[8][8]
        # cromosome[6][4], cromosome[7][5] = cromosome[7][5], cromosome[6][4]
        cromosome[8][7], cromosome[6][6] = cromosome[6][6], cromosome[8][7]
        # cromosome[3][0], cromosome[4][2] = cromosome[4][2], cromosome[3][0]
        # cromosome[3][4], cromosome[4][4] = cromosome[4][4], cromosome[3][4]
        # cromosome[0][7], cromosome[0][8] = cromosome[0][8], cromosome[0][7]

    return cromosome


def genetic_algorithm(pop_size):
    """
    - The funtion of iterations to loop over generations.
    :param pop_size: the number of chromosomes I want in a loop.
    :return: nothing.
    """
    population = making_population(pop_size)
    found = False
    generation = 1

    while not found:
        population = sorting(population)
        if fitness(population[0]) == 0:
            found = True
            break

        generated_population = []
        scaled_factor = int(pop_size * 0.5)
        generated_population = population[:scaled_factor]

        s1 = int(20 * len(generated_population) / 100)
        for j in range(s1):
            # choose two random integers in selection_size
            a = np.random.randint(0, len(generated_population))
            b = np.random.randint(0, len(generated_population))
            # perform crossover on the chosen chromosomes
            generated_population = crossover(generated_population, generated_population[a], generated_population[b], 0.1)

        s2 = int(30 * len(generated_population) / 100)
        for k in range(s2):
            crom = np.random.randint(0, len(generated_population))
            mutation = random_mutation(generated_population[crom], .05)
            generated_population.append(mutation)

        population = generated_population

        print("Generation: ", generation, "\n", population[0], "  --> Fitness: ", fitness(population[0]))

        generation += 1


if __name__ == '__main__':
    # input_matrix = taking_input()
    # chromosome = creating_chromosome(input_matrix)
    # population = making_population(100)

    # print(chromosome[0])
    # print(chromosome[1])
    # print(chromosome[2])
    # print(chromosome[3])
    # print(chromosome[4])
    # print(chromosome[5])
    # print(chromosome[6])
    # print(chromosome[7])
    # print(chromosome[8])
    #
    t1 = time.time()

    genetic_algorithm(30000)
    t2 = time.time()
    print("It toke: ", t2 - t1)

# The last sudoko matrix I tried here is :
# 0
# 0
# 9
# 0
# 0
# 0
# 1
# 0
# 0
# 2
# 1
# 7
# 0
# 0
# 0
# 3
# 6
# 8
# 0
# 0
# 0
# 2
# 0
# 7
# 0
# 0
# 0
# 0
# 6
# 4
# 1
# 0
# 3
# 5
# 8
# 0
# 0
# 7
# 0
# 0
# 0
# 0
# 0
# 0
# 0
# 1
# 5
# 0
# 4
# 2
# 8
# 0
# 7
# 9
# 0
# 0
# 0
# 5
# 8
# 9
# 0
# 0
# 0
# 4
# 8
# 5
# 0
# 0
# 0
# 2
# 9
# 3
# 0
# 0
# 6
# 3
# 0
# 2
# 8
# 0
# 0
