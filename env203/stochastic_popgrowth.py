# ENVSCI 203 Stochastic Population Growth Model
# Created for assignment 3
#   seperated from other model for debugging
#
# Created by Samuel Kolston
# Created on: 230920
# Last edited: 230920 1307
#


# modules
import matplotlib.pyplot as plt
import random
import numpy as np

# constants
RD = 0.5
K = 2000
T = 50
N_0 = K
Q = 250
E = 0.25
S = 0.5
ISOLATED_SIMS = 10


# performs the base logistic calculation with stochasticity
def stochastic_log(nt, growth_rate, carry_cap, sd):
    return nt + (growth_rate + growth_rate * sd) * nt * (1 - nt / carry_cap)


# calculates S * D for stochasticity
def randbetween(s_value):
    return s_value * (random.randint(-1000, 1000) / 1000)


# checks if harvest is absolute
def max_0(harvest):
    if harvest >= 0:
        return harvest
    else:
        return 0


# runs all models using gen_log with modifiers and checks for abs values
def extract(sim_list, index):
    return [item[index] for item in sim_list]


def plotter(plt, title, xlabel, ylabel, series, labels, colours, legend):
    plt.set_title(title)
    plt.set_xlabel(xlabel)
    plt.set_ylim(0 - 100, K + 100)
    plt.set_ylabel(ylabel)
    for n_data in range(len(series)):
        plt.plot(series[n_data], label=labels[n_data], color=colours[n_data])
    plt.legend(ncol=2, bbox_to_anchor=(legend[0], legend[1]), loc="upper center")


simulations = []
for i in range(ISOLATED_SIMS):
    tmp = [N_0]
    for model in range(T - 1):
        # tmp.append(max_0((tmp[-1] + (RD + RD * randbetween(S)) * tmp[-1] * (1 - tmp[-1] / K) - E * tmp[-1])))
        tmp.append(max_0((tmp[-1] + (RD + RD * randbetween(S)) * tmp[-1] * (1 - tmp[-1] / K) - Q)))
    simulations.append(tmp)

means = []
stds = []
std_pos = []
std_neg = []

for n in range(T):
    means.append(np.mean(extract(simulations, n)))
    stds.append(np.std(extract(simulations, n)))

for i in range(len(means)):
    std_pos.append(means[i] + stds[i])
    std_neg.append(means[i] - stds[i])

figure, subp = plt.subplots(num=2, nrows=1, ncols=1, figsize=(10, 8))
figure.canvas.set_window_title("Figure 3: LHM with Stochasticity")
plt.suptitle("Population of Fish over {} years with stochasticity".format(T), fontsize=14)

plotter(subp, "title?", "Years (t)", "Population", [means, std_neg, std_pos],
        ["Average", "Average + Standard Deviation", "Average - Standard Deviation"], ["red", "grey", "grey"],
        [0.5, -0.2])

plt.show()
