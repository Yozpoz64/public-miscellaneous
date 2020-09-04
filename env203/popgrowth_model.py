# ENVSCI 203 Population Growth Model
# Created for assignment 3
#
# Created by Samuel Kolston
# Created on: 290820
# Last edited: 040920 165100
#
# TO DO
# -combine plotting and subplotting functions

# modules
import matplotlib.pyplot as plt
import random

# constants
RD = 0.5
K = 2000
T = 50
N_0 = 1
Q = 250
E = 0.5
S = 0.1
# constants for debugging
SHOW_STATUS = False
SHOW_PLOTS = True


# dict for model values and associated plot preferences
plots = \
    {
        "unharvested":
            {
                "label": "Unharvested",
                "colour": "blue",
                "values": [N_0],
                "delta nt": []
            },
        "fq":
            {
                "label": "Fixed-quota",
                "colour": "pink",
                "values": [K],
                "actual harvest": []
            },
        "fe":
            {
                "label": "Fixed-effort",
                "colour": "green",
                "values": [K],
                "effort line": [],
                "actual harvest": []
            },
        "fq_s":
            {
                "label": "Stochastic Fixed-quota",
                "colour": "pink",
                "sd": [],
                "values": [K],
                "actual harvest": []
            },
        "fe_s":
            {
                "label": "Stochastic Fixed-effort",
                "colour": "green",
                "sd": [],
                "values": [K],
                "effort line": [],
                "actual harvest": []
            },
        "k":
            {
                "label": "Carrying Capacity",
                "colour": "red",
                "values": [],
            },
        "t":
            {
                "label": "Years",
                "colour": "blue",
                "values": [],
            },
        "q":
            {
                "label": "Quota",
                "colour": "orange",
                "values": [],
            },
    }


# function that performs the base logistic calculation
def gen_log(nt, growth_rate, carry_cap):
    return nt + growth_rate * nt * (1 - nt / carry_cap)


# function that performs the base logistic calculation with stochasticity
def stochastic_log(nt, growth_rate, carry_cap, sd):
    return nt + (growth_rate + growth_rate * sd) * nt * (1 - nt / carry_cap)


# function that calculates S * D for stochasticity
def randbetween(s_value):
    return s_value * (random.randint(-1000, 1000) / 1000)


# function that checks if harvest is absolute
def max_0(harvest, harvest_list):
    if harvest >= 0:
        harvest_list.append(harvest)
    else:
        harvest_list.append(0)


# calculates actual harvest
def actual_harvest(harvest, state, actharvest_list):
    if harvest > state:
        actharvest_list.append(state)
    else:
        actharvest_list.append(harvest)


# plots data to subplots
def subplotter(plot, sp_x, sp_y, title, xlabel, ylabel, series, labels, colours):
    plot[sp_x][sp_y].set_title(title)
    plot[sp_x][sp_y].set_xlabel(xlabel)
    plot[sp_x][sp_y].set_ylabel(ylabel)
    for n_data in range(len(series)):
        plot[sp_x][sp_y].plot(series[n_data], label=labels[n_data], color=colours[n_data])
    plot[sp_x][sp_y].legend(ncol=2, bbox_to_anchor=(0.5, -0.15), loc="upper center")


# plots data to individual plot
def plotter(plot, title, xlabel, ylabel, series, labels, colours):
    plot.set_title(title)
    plot.set_xlabel(xlabel)
    plot.set_ylabel(ylabel)
    for n_data in range(len(series)):
        plot.plot(series[n_data], label=labels[n_data], color=colours[n_data])
    subp.legend(ncol=2, bbox_to_anchor=(0.5, -0.08), loc="upper center")


# add some parameters to lists for plotting
for time in range(T + 1):
    plots["k"]["values"].append(K)
    plots["t"]["values"].append(time)
    plots["q"]["values"].append(Q)

# runs all models using gen_log with modifiers and checks for abs values
for model in range(T):
    # unharvested
    plots["unharvested"]["values"].append(gen_log(plots["unharvested"]["values"][-1], RD, K))
    plots["unharvested"]["delta nt"].append(plots["unharvested"]["values"][-1] - plots["unharvested"]["values"][-2])

    # quota harvesting
    max_0(gen_log(plots["fq"]["values"][-1], RD, K) - Q, plots["fq"]["values"])

    # effort harvesting
    max_0(gen_log(plots["fe"]["values"][-1], RD, K) - E * plots["fe"]["values"][-1], plots["fe"]["values"])
    plots["fe"]["effort line"].append(E * plots["unharvested"]["values"][-1])

    # stochastic quota harvesting
    plots["fq_s"]["sd"].append(randbetween(S))
    max_0(stochastic_log(plots["fq_s"]["values"][-1], RD, K, plots["fq_s"]["sd"][-1]) - Q, plots["fq_s"]["values"])

    # stochastic effort harvesting
    plots["fe_s"]["sd"].append(randbetween(S))
    max_0(stochastic_log(plots["fe_s"]["values"][-1], RD, K, plots["fe_s"]["sd"][-1]) - E * plots["fe_s"]["values"][-1],
          plots["fe_s"]["values"])

# calculates actual harvest if applicable
for i in range(T + 1):
    actual_harvest(plots["fq"]["values"][i], Q, plots["fq"]["actual harvest"])
    actual_harvest(plots["fe"]["values"][i], E * plots["fe"]["values"][i], plots["fe"]["actual harvest"])
    actual_harvest(plots["fq_s"]["values"][i], Q, plots["fq_s"]["actual harvest"])
    actual_harvest(plots["fe_s"]["values"][i], E * plots["fe_s"]["values"][i], plots["fe_s"]["actual harvest"])

if SHOW_PLOTS:
    # LHM plots
    figure, subp = plt.subplots(num=1, nrows=2, ncols=2, figsize=(12, 10))
    figure.canvas.set_window_title("Figure 1: LHM")
    plt.suptitle("Population of Fish over {} years".format(T), fontsize=14)

    # plot data in subplots
    subplotter(subp, 0, 0, plots["unharvested"]["label"], plots["t"]["label"], "Population",
            [plots["unharvested"]["values"], plots["unharvested"]["delta nt"]], ["N", "Growth Rate"],
            [plots["unharvested"]["colour"], "red"])
    subplotter(subp, 0, 1, "Harvested", plots["t"]["label"], "Population", [plots["fq"]["values"], plots["fe"]["values"]],
            [plots["fq"]["label"], plots["fe"]["label"]], [plots["fq"]["colour"], plots["fe"]["colour"]])
    subplotter(subp, 1, 0, "Quota vs Actual Harvest (Fixed-quota)", plots["t"]["label"], "Population Harvest",
            [plots["q"]["values"], plots["fq"]["actual harvest"]], ["Quota", "Actual Harvest"], ["black", "brown"])
    subplotter(subp, 1, 1, "Fixed-effort Actual Harvest", plots["t"]["label"], "Population Harvest",
            [plots["fe"]["actual harvest"]], ["Actual Harvest"], ["navy"])

    # display constant values below plot
    plt.gcf().text(0.5, 0.05, "where:\n$r_d$={}     $K$={}     $T$={}     $Q$={}     $E$={}"
                   .format(RD, K, T, Q, E), fontsize=12, ha="center")

    # adjust plots with spacing
    figure.tight_layout(pad=3)
    plt.subplots_adjust(left=None, bottom=0.2, right=0.9, top=None, wspace=None, hspace=None)

    # LHM with stochasticity plots
    figure, subp = plt.subplots(num=2, nrows=1, ncols=1, figsize=(10, 8))
    figure.canvas.set_window_title("Figure 2: LHM with Stochasticity")
    plt.suptitle("Population of Fish over {} years with stochasticity".format(T), fontsize=14)

    # plot data
    plotter(subp, "Harvesting With Stochasticity", plots["t"]["label"], "Population Harvest",
            [plots["fq_s"]["values"], plots["fe_s"]["values"]],
            [plots["fq_s"]["label"], plots["fe_s"]["label"]], [plots["fq"]["colour"], plots["fe"]["colour"]])

    # display constant values below plot
    plt.gcf().text(0.5, 0.05, "where:\n$r_d$={}     $K$={}     $T$={}     $Q$={}     $E$={}     $S$={}"
                   .format(RD, K, T, Q, E, S), fontsize=12, ha="center")

    # adjust plots with spacing
    figure.tight_layout(pad=3)
    plt.subplots_adjust(left=None, bottom=0.2, right=0.9, top=None, wspace=None, hspace=None)

# print model output
if SHOW_STATUS:
    print("unharvested output: ", plots["unharvested"]["values"])
    print("unharvested change: ", plots["unharvested"]["delta nt"])
    print("\nfixed quota output: ", plots["fq"]["values"])
    print("fixed quota actual harvest: ", plots["fq"]["actual harvest"])
    print("\nfixed effort output: ", plots["fe"]["values"])
    print("fixed effort actual harvest: ", plots["fe"]["actual harvest"])
    print("fixed effort effort line: ", plots["fe"]["effort line"])
    print("\nfixed quota stochastic sd: ", plots["fq_s"]["sd"])
    print("fixed quota stochastic output: ", plots["fq_s"]["values"])
    print("fixed quota actual harvest: ", plots["fq_s"]["actual harvest"])
    print("\nfixed effort stochastic sd: ", plots["fe_s"]["sd"])
    print("fixed effort stochastic output: ", plots["fe_s"]["values"])
    print("fixed effort stochastic actual harvest: ", plots["fe_s"]["actual harvest"])
    print("fixed effort stochastic effort line: ", plots["fe_s"]["effort line"])

# show figures and plots
plt.show()
