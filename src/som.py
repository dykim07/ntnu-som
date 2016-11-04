#!/usr/bin/env python3

from decay import StaticDecay, LinearDecay, ExponentialDecay
from helper import read_data, plot_map
import random

def main():
    cities = read_data('western_sahara')

    learning_rate = ExponentialDecay(0.8, 0.9999)
    run_som(cities, 25000, learning_rate)


def run_som(cities, iterations, learning_rate):
    # Initialize the weights of the neurons
    # neurons = [[14000, 24000]]
    # for i in range(1, len(cities) * 4):
    #     neurons.append([neurons[i-1][0] + 10,
    #                     neurons[i-1][1] + 10])
    neurons = []
    range_argument = int(len(cities) / 2)
    for i in range(len(cities) * 4):
        neurons.append([random.randint(9700, 24700),
                        random.randint(20833, 27470)])

    for i in range(iterations):
        # Pick a random city
        city = cities[i % len(cities)]
        # Choose the winner neuron
        winner, winner_index = choose_winner(city, neurons)
        # Update the weights of the neuron and its neighbourhood
        for j in range(-range_argument, range_argument):
            k = (winner_index + j) % len(neurons)
            neighbour = 1.0 / (abs(j)+1) * 2
            neurons[k][0] += learning_rate.value * neighbour * (city[0] - neurons[k][0])
            neurons[k][1] += learning_rate.value * neighbour * (city[1] - neurons[k][1])

        if i % 2000 == 0:
            range_argument -= 1

        if i < 10000 and i % 250 == 0 or i % 2500 == 0:
            plot_map(cities, neurons, i)
        # Update the learning rate
        learning_rate.decay()

    plot_map(cities, neurons, iterations)

def manhattan_distance(center, neuron):
    return abs(center[0] - neuron[0]) + abs(center[1] - neuron[1])

def choose_winner(city, neurons):
    minimum = 1000000
    index = 0
    for i in range(len(neurons)):
        distance = manhattan_distance(city, neurons[i])
        if distance < minimum:
            winner = neurons[i]
            minimum = distance
            index = i
    return winner, index


if __name__ == '__main__': main()