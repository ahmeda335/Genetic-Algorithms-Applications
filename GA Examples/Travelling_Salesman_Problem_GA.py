# ------------------------------------------------------ #
# ----------- Travelling-Salesman-Problem -------------- #
# ------------------------------------------------------ #

# - Travelling Salesman Problem is a famous problem that you want to get
# the smallest path which this salesman can go through such that he visits
# all cities only one time and then returns to the first city again.

# - You can solve it using many methods, Genetic Algorithms is one of the best.

import random
import numpy as np

class Travelling_Salesman_Proplem:
    def __init__(self, citiesNumber, distances):
        self.cities_number = citiesNumber
        self.distances = distances
        self.pop_size = 5000
        self.generation_times = 50

    def taking_input(self):
        """
        - This function is used to take the input from the user in a list of lists,
        such that each sublist is the distances from this number of city and the other
        cities.
        :return: distances between all cities (list of lists).
        """
        distances = input("Enter the distances between the cities in list of lists: ")
        return distances


    def generating_chromosome(self):
        """
        - Genetic Algorithm depends mainly on creating a random solution (chromosome),
        then improving it. This function makes this random, the shape of this chromosome
        depends on the problem.
        :return: one chromosome (random solution)
        """
        global cities_num
        chrom = [0]
        for i in range(cities_num - 1):
            a = np.random.randint(1, cities_num)
            while a in chrom:
                a = np.random.randint(1, cities_num)
            chrom.append(a)
        chrom.append(0)
        return chrom


    def creating_population(self):
        """
        - Creating lots of chromosomes (of course, I won't make only one random solution -chromosome-)
        to improve them.
        :param pop_size: Number of chromosomes I want to create.
        :return: population of chromosomes (random solutions)
        """
        pop = []
        for i in range(self.pop_size):
            pop.append(self.generating_chromosome())

        return pop


    def fittest_fun(self, chromosome):
        """
        - This is the function that I detect throught if the solution is near or
        far from the optimal solution. It depends on the problem.
        :param chromosome: one of the random solutions
        :return: number detecting the fitness of the solution.
        """
        global distances
        fin = float('inf')
        fittest = 0
        for i in range(len(chromosome) - 1):
            fittest += distances[chromosome[i]][chromosome[i + 1]]

        return fittest


    def selection(self, population, scale):
        """
        - The first step in the Genetic Algorithm method. I select some of the population (solutions).
        I try to select the fittest ones.
        :param population: the solutions I have
        :param scale: percentage of the solutions I want to select.
        :return: the selected population.
        """
        selected_pop = population[0:int(scale * len(population))]
        return selected_pop


    def crossover(self, population, pc):
        """
        - The second step in GA. I generate new offstring (children) from current solutions (parents).
        There are many methods to do that depending on the problem.
        :param population: the solutions
        :param pc: probability of crossover, I use to minimize the probability of the crossover. I can change it.
        :return: the new offspring.
        """
        a = random.randint(0, len(population) - 1)
        b = random.randint(0, len(population) - 1)
        parent1 = population[a]
        parent2 = population[b]

        if np.random.rand() < pc:
            cut = random.randint(1, len(population[0]) - 1)
            child1 = parent1[:cut]
            child1 += [city for city in parent2 if city not in child1]
            child1 += [parent1[-1]]
            population.append(child1)

            child2 = parent2[:cut]
            child2 += [city for city in parent1 if city not in child2]
            child2 += [parent2[-1]]
            population.append(child2)

        return population


    def mutation(self, population, pm):
        """
        - The third and last step in GA. I make to increase the exploration of the search space,
        by increasing diversity and try to avoid local optima.
        :param population: the solutions I have.
        :param pm: probability of mutation, I use to minimize the probability of the mutation. I can change it.
        :return: the population.
        """

        # I randomly select two genes in the chromosome and swap them, except the first and the last genes.
        global cities_num
        if np.random.rand() < pm:
            rand_num = np.random.randint(int(len(population)/2), len(population))
            rand_pos1 = np.random.randint(1, cities_num)
            rand_pos2 = np.random.randint(1, cities_num)

            population[rand_num][rand_pos1], population[rand_num][rand_pos2] = population[rand_num][rand_pos2],\
                                                                               population[rand_num][rand_pos1]
        return population


    def stopping_function(self, best_values):
        """
        - This is a helper function that it detects if the the optimal solution is getten or a local optima,
        so that it will close the program.
        :param best_values: the best solution tell now
        :return: boolean value.
        """
        if len(best_values[-5:]) - len(set(best_values[-5:])) >= 7:
            return True
        return False


    def generating_algorithm(self):
        """
        - The main funciton to make the generation process for many times.
        :param generation_times: Number of generations I want to create
        :param pop_size: Number of initial solutions (chromosomes) I want to create.
        :return: nothing.
        """
        # Generating the population.
        population = self.creating_population()
        best_values = []
        generation = 1

        for i in range(self.generation_times):
            # Gitting the fittness of all chromosomes in the population.
            population = sorted(population, key=self.fittest_fun)

            # Making selection to select the most fittest chromosomes from the population
            scale1 = 0.5
            generated_population = self.selection(population, scale1)

            # When getting to a single solution.
            if len(population) <= 1:
                break

            # Making crossover to generate offsprings.
            scale2 = 1
            for j in range(int(len(generated_population) * scale2)):
                pc = 0.25
                generated_population = self.crossover(generated_population, pc)

            # Making mutation, swapping randomly.
            scale3 = 1
            for k in range(int(len(generated_population) * scale3)):
                pm = 0.1
                generated_population = self.mutation(generated_population, pm)

            population = generated_population
            print("number of population is: ", len(population))
            best_values.append(self.fittest_fun(population[0]))

            # If getting to the best solution or in local minima.
            if self.stopping_function(best_values):
                break

            # printing the loops.
            print("Generation: ", generation)
            print("Path is: ", ' --> '.join(map(str, population[0])),
                  "\nwith distance: ", self.fittest_fun(population[0]), "\n")
            generation += 1


if __name__ == '__main__':
    # cities_num = int(input("Write the number of cities: "))
    # distances = taking_input()

    inf = float('inf')
    distances = [
        [0, 2, inf, 12, 5, 6, 20, 10, 9, 12],
        [2, 0, 4, 8, inf, 3, inf, 19, 20, 31],
        [inf, 4, 0, 3, 3, 3, 9, 9, 10, 32],
        [12, 8, 3, 0, 10, 22, 1, 20, inf, 21],
        [5, inf, 3, 10, 0, 3, 2, 12, 2, 9],
        [3, 9, 19, inf, 10, 0, 20, 88, 22, 1],
        [2, 3, 4, 1, 39, 12, 0, 12, 12, 11],
        [12, 22, 1, 19, 29, 22, 1, 0, 3, 1],
        [8, inf, 29, 11, 29, 1, 19, 29, 0, 22],
        [3, 19, 12, 92, 19, inf, 2, 3, 11, 0]
    ]
    cities_num = 10

    TSP = Travelling_Salesman_Proplem(cities_num, distances)
    TSP.generating_algorithm()

    # By many runs for the program, I thing that the optimal solution is '22' for the above example.
