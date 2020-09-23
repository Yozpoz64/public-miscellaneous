# ENVSCI 203 Stochastic Population Growth Model
# Created for assignment 3
#   seperated from other model for debugging
#
# Created by Samuel Kolston
# Created on: 230920
# Last edited: 230920 1704

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

# nested dict for values
data = {
    "fe_s": {
        "simulations": [],
        "averages": [],
        "stdevs": [],
        "std_pos": [],
        "std_neg": [],
    },
    "fe_d": {
        "values": [N_0],
    },
    "fq_s": {
        "simulations": [],
        "averages": [],
        "stdevs": [],
        "std_pos": [],
        "std_neg": [],
    },
    "fq_d": {
        "values": [N_0],
    },
}


# checks if harvest is absolute
def max_0(harvest):
    if harvest >= 0:
        return harvest
    else:
        return 0


# performs the base logistic calculation
def gen_log(nt, growth_rate, carry_cap):
    return nt + growth_rate * nt * (1 - nt / carry_cap)


# performs the stochastic logistic calculation for both harvesting methods
def stochastic_log(nt, growth_rate, carry_cap, sd, type):
    if type == "effort":
        return max_0(nt + (growth_rate + growth_rate * sd) * nt * (1 - nt / carry_cap) - E * nt)
    elif type == "quota":
        return max_0(nt + (growth_rate + growth_rate * sd) * nt * (1 - nt / carry_cap) - Q)


# calculates S * D for stochasticity
def randbetween(s_value):
    return s_value * (random.randint(-1000, 1000) / 1000)


# takes x index value from every key in a nested list
def extract(sim_list, index):
    return [item[index] for item in sim_list]


# plots data, creates legend
def plotter(plt, index, title, xlabel, ylabel, series, labels, colours, legend):
    cur_plt = plt[index]
    cur_plt.set_title(title)
    cur_plt.set_xlabel(xlabel)
    cur_plt.set_ylim(0 - 100, K + 100)
    cur_plt.set_ylabel(ylabel)
    for n_data in range(len(series)):
        cur_plt.plot(series[n_data], label=labels[n_data], color=colours[n_data])
    cur_plt.legend(ncol=2, bbox_to_anchor=(legend[0], legend[1]), loc="upper center")


# calculate deterministic values
for baseline in range(T):
    data["fq_d"]["values"].append(gen_log(data["fq_d"]["values"][-1], RD, K) - Q)
    data["fe_d"]["values"].append(gen_log(data["fe_d"]["values"][-1], RD, K) - E * data["fe_d"]["values"][-1])

# calculate stochastic values (as many times as specified)
for i in range(ISOLATED_SIMS):
    tmp_fq_list = [N_0]
    tmp_fe_list = [N_0]
    for model in range(T + 1):
        tmp_fq_list.append(stochastic_log(tmp_fq_list[-1], RD, K, randbetween(S), "quota"))
        tmp_fe_list.append(stochastic_log(tmp_fe_list[-1], RD, K, randbetween(S), "effort"))
    data["fq_s"]["simulations"].append(tmp_fq_list)
    data["fe_s"]["simulations"].append(tmp_fe_list)

# add averages and standard deviations together for plotting
for n in range(T + 1):
    data["fe_s"]["averages"].append(np.mean(extract(data["fe_s"]["simulations"], n)))
    data["fe_s"]["stdevs"].append(np.std(extract(data["fe_s"]["simulations"], n)))
    data["fe_s"]["std_pos"].append(data["fe_s"]["averages"][n] + data["fe_s"]["stdevs"][n])
    data["fe_s"]["std_neg"].append(data["fe_s"]["averages"][n] - data["fe_s"]["stdevs"][n])

    data["fq_s"]["averages"].append(np.mean(extract(data["fq_s"]["simulations"], n)))
    data["fq_s"]["stdevs"].append(np.std(extract(data["fq_s"]["simulations"], n)))
    data["fq_s"]["std_pos"].append(data["fq_s"]["averages"][n] + data["fq_s"]["stdevs"][n])
    data["fq_s"]["std_neg"].append(data["fq_s"]["averages"][n] - data["fq_s"]["stdevs"][n])

# create figure and plot data
figure, subp = plt.subplots(num=2, nrows=1, ncols=2, figsize=(15, 7))
figure.canvas.set_window_title("Figure 3: LHM with Stochasticity")
plt.suptitle("Population of Fish over {} years with stochasticity".format(T), fontsize=14)
plotter(subp, 0, "Fixed-quota Stochastic Harvesting", "Years (t)", "Population (N)",
        [data["fq_s"]["averages"], data["fq_d"]["values"], data["fq_s"]["std_pos"], data["fq_s"]["std_neg"]],
        ["Average (N)", "Deterministic (N)", "Average + Standard Deviation", "Average - Standard Deviation"],
        ["red", "black", "grey", "grey"], [0.3, -0.15])
plotter(subp, 1, "Fixed-effort Stochastic Harvesting", "Years (t)", "Population (N)",
        [data["fe_s"]["averages"], data["fe_d"]["values"], data["fe_s"]["std_pos"], data["fe_s"]["std_neg"]],
        ["Average (N)", "Deterministic (N)", "Average + Standard Deviation", "Average - Standard Deviation"],
        ["green", "black", "grey", "grey"], [0.7, -0.15])
plt.gcf().text(0.5, 0.02, "where:\n$r_d$={}     $K$={}     $T$={}     $N_0$={}\n$S$={}     $E$={}\nModel run {} times"
               .format(RD, K, T, N_0, S, E, ISOLATED_SIMS), fontsize=10, ha="center")
figure.tight_layout(pad=3)
plt.subplots_adjust(left=None, bottom=0.2, right=0.9, top=None, wspace=None, hspace=None)

# show plot
plt.show()
