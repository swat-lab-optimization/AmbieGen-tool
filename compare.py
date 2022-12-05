
import os
import argparse

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import MaxNLocator

def parse_arguments():
    """
    This function parses the arguments passed to the script
    :return: The arguments that are being passed to the program
    """

    print("Parsing the arguments")
    parser = argparse.ArgumentParser(
                    prog = 'optimize.py',
                    description = 'A tool for generating test cases for autonomous systems',
                    epilog = "For more information, please visit ")
    # parse a list of arguments
    parser.add_argument('--stats_path', nargs='+', help='The source folders of the metadate to analyze', required=True)
    parser.add_argument('--stats_names', nargs='+', help='The names of the corresponding algorithms', required=True)
    in_arguments = parser.parse_args()
    return in_arguments



def plot_convergence(dfs, stats_names):
    """
    Function for plotting the convergence of the algorithms
    It takes a list of dataframes and a list of names for the dataframes, and plots the mean and
    standard deviation of the dataframes
    
    :param dfs: a list of dataframes, each containing the mean and standard deviation of the fitness of
    the population at each generation
    :param stats_names: The names of the algorithms
    """
    fig, ax = plt.subplots()

    plt.xlabel("Number of generations", fontsize=16)
    plt.ylabel("Fitness", fontsize=16)

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.grid()

    for i, df in enumerate(dfs):
        x = np.arange(0, len(dfs[i]["mean"]))
        plt.plot(x, dfs[i]["mean"], label=stats_names[i])
        plt.fill_between(x, dfs[i]["mean"] - dfs[i]["std"], dfs[i]["mean"] + dfs[i]["std"], alpha=0.2)
        plt.legend()
    plt.savefig('convergence.png')

def plot_boxplot(data_list, label_list, name, max_range):
    """
     Function for plotting the boxplot of the statistics of the algorithms
    It takes a list of lists, a list of labels, a name, and a max range, and plots a boxplot of the data
    
    :param data_list: a list of lists, each list containing the data for a particular algorithm
    :param label_list: a list of labels, each label corresponding to the data in the data_list
    :param name: the name of the plot
    :param max_range: the maximum value of the y-axis
    """

    fig, ax1 = plt.subplots() #figsize=(8, 4)
    ax1.set_xlabel('Algorithm', fontsize=20)
    ax1.set_ylabel(name, fontsize=20)
    

    ax1.tick_params(axis="both", labelsize=18)
    
    ax1.yaxis.grid(True, linestyle='-', which='both', color='darkgray', linewidth=2, alpha=0.5)

    top = max_range
    bottom = 0
    ax1.set_ylim(bottom, top)
    ax1.boxplot(data_list, widths=0.3, labels=label_list)

    plt.subplots_adjust(bottom=0.15)

    fig.savefig(name + ".png")


def main(stats_path, stats_names):
    """
    Main function for building plots comparing the algorithms
    It takes a list of paths to folders containing the results of the tool runs, and a list of names
    of the runs, and it plots the convergence and the boxplots of the fitness and novelty
    
    :param stats_path: a list of paths to the folders containing the stats files
    :param stats_names: list of strings, names of the runs
    """
    convergence_paths = []
    stats_paths = []
    for path in stats_path:
        for file in os.listdir(path):
            if "conv" in file:
                convergence_paths.append(os.path.join(path, file))
            if "stats" in file:
                stats_paths.append(os.path.join(path, file))

    dfs = {}
    for i, file in enumerate(convergence_paths):
        with open(file, 'r', encoding="utf-8") as f:
            data = json.load(f)
        dfs[i] = pd.DataFrame(data=data)
        dfs[i]["mean"] = dfs[i].mean(axis=1)
        dfs[i]["std"] = dfs[i].std(axis=1)
    
    plot_convergence(dfs, stats_names)

    fitness_list = []
    novelty_list = []
    for i, file in enumerate(stats_paths):
        with open(file, 'r', encoding="utf-8") as f:
            data = json.load(f)
        results_fitness = []
        results_novelty = []
        for m in range(len(data)):
            results_fitness.extend(data["run"+str(m)]["fitness"])
            results_novelty.append(data["run"+str(m)]["novelty"])
        fitness_list.append(results_fitness)
        novelty_list.append(results_novelty)

    plot_boxplot(fitness_list, stats_names, "fitness", 20)
    plot_boxplot(novelty_list, stats_names, "novelty", 1)

if __name__ == "__main__":
    arguments = parse_arguments()
    stats_path = arguments.stats_path
    stats_names = arguments.stats_names

    main(stats_path, stats_names)