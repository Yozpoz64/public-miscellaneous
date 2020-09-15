# ENVSCI 203 Population Growth Model
# Created for assignment 3
#
# Created by Samuel Kolston
# Created on: 290820
# Last edited: 040920 204400
#
# TO DO
# -standard dev and other plotted calculations

# modules
import matplotlib.pyplot as plt
import random

# constants
RD = 0.5
K = 2000
T = 50
N_0 = 100
Q = 250
E = 0.5
S = 0.1
# constants for debugging
SHOW_STATUS = False
ISSUE = 3  # changes plot output for assignment (0 for old SHOW_PLOT)


# dict for model values and associated plot preferences
plots = \
    {
        "unharvested":
            {
                "label": "Unharvested",
                "colour": "blue",
                "values": [N_0],
                "values rd1": [N_0],
                "values rd2": [N_0],
                "delta nt": [0],
                "delta nt1": [0],
                "delta nt2": [0]
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


# performs the base logistic calculation
def gen_log(nt, growth_rate, carry_cap):
    return nt + growth_rate * nt * (1 - nt / carry_cap)


# performs the base logistic calculation with stochasticity
def stochastic_log(nt, growth_rate, carry_cap, sd):
    return nt + (growth_rate + growth_rate * sd) * nt * (1 - nt / carry_cap)


# calculates S * D for stochasticity
def randbetween(s_value):
    return s_value * (random.randint(-1000, 1000) / 1000)


# checks if harvest is absolute
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


# plots data, creates legend
def plotter(plot, is_subplot, origin, title, xlabel, ylabel, series, labels, colours, legend):
    if is_subplot:
        if len(origin) > 1:
            tmp = plot[origin[0]][origin[1]]
        else:
            tmp = plot[origin[0]]
    else:
        tmp = plot
    tmp.set_title(title)
    tmp.set_xlabel(xlabel)
    tmp.set_ylabel(ylabel)
    for n_data in range(len(series)):
        tmp.plot(series[n_data], label=labels[n_data], color=colours[n_data])
    tmp.legend(ncol=2, bbox_to_anchor=(legend[0], legend[1]), loc="upper center")


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

    # unharvested with different rd values TEMP
    plots["unharvested"]["values rd1"].append(gen_log(plots["unharvested"]["values rd1"][-1], 0, K))
    plots["unharvested"]["delta nt1"].append(plots["unharvested"]["values rd1"][-1] - plots["unharvested"]["values rd1"][-2])
    plots["unharvested"]["values rd2"].append(gen_log(plots["unharvested"]["values rd2"][-1], -0.5, K))
    plots["unharvested"]["delta nt2"].append(plots["unharvested"]["values rd2"][-1] - plots["unharvested"]["values rd2"][-2])

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

# combo of most plots (used for debugging)
if ISSUE == 0:
    # LHM plots
    figure, subp = plt.subplots(num=1, nrows=2, ncols=2, figsize=(12, 10))
    figure.canvas.set_window_title("Figure 1: LHM")
    plt.suptitle("Population of Fish over {} years".format(T), fontsize=14)

    # plot data in subplots
    plotter(subp, True, [0, 0], plots["unharvested"]["label"], plots["t"]["label"], "Population",
            [plots["unharvested"]["values"], plots["unharvested"]["delta nt"]], ["N", "Growth Rate"],
            [plots["unharvested"]["colour"], "red"], [0.5, -0.2])
    plotter(subp, True, [0, 1], "Harvested", plots["t"]["label"], "Population", [plots["fq"]["values"], plots["fe"]["values"]],
            [plots["fq"]["label"], plots["fe"]["label"]], [plots["fq"]["colour"], plots["fe"]["colour"]], [0.5, -0.2])
    plotter(subp, True, [1, 0], "Quota vs Actual Harvest (Fixed-quota)", plots["t"]["label"], "Population Harvest",
            [plots["q"]["values"], plots["fq"]["actual harvest"]], ["Quota", "Actual Harvest"], ["black", "brown"],
                [0.5, -0.2])
    plotter(subp, True, [1, 1], "Fixed-effort Actual Harvest", plots["t"]["label"], "Population Harvest",
            [plots["fe"]["actual harvest"]], ["Actual Harvest"], ["navy"], [0.5, -0.2])

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
    plotter(subp, False, 0, "Harvesting With Stochasticity", plots["t"]["label"], "Population Harvest",
            [plots["fq_s"]["values"], plots["fe_s"]["values"]],
            [plots["fq_s"]["label"], plots["fe_s"]["label"]], [plots["fq"]["colour"], plots["fe"]["colour"]],
                [0.5, -0.08])

    # display constant values below plot
    plt.gcf().text(0.5, 0.03, "where:\n$r_d$={}     $K$={}     $T$={}     $Q$={}     $E$={}     $S$={}"
                   .format(RD, K, T, Q, E, S), fontsize=12, ha="center")

    # adjust plots with spacing
    figure.tight_layout(pad=3)
    plt.subplots_adjust(left=None, bottom=0.2, right=0.9, top=None, wspace=None, hspace=None)

# issue 1 - unharvested
elif ISSUE == 1:
    figure, subp = plt.subplots(num=2, nrows=1, ncols=2, figsize=(15, 6))
    figure.canvas.set_window_title("Figure 1: LHM")
    plt.suptitle("Population of Fish over {} years (at various rates of growth)".format(T), fontsize=14)

    plotter(subp, True, [0], "Unharvested Population", plots["t"]["label"], "Population",
            [plots["unharvested"]["values"], plots["unharvested"]["values rd1"], plots["unharvested"]["values rd2"]], ["N ($r_d=0.5$)", "N ($r_d=0$)", "N ($r_d=-0.5$)"],
            ["blue", "green", "red"], [0.3, -0.11])

    plotter(subp, True, [1], "Unharvested Change in Population", plots["t"]["label"], "Population",
            [plots["unharvested"]["delta nt"], plots["unharvested"]["delta nt1"], plots["unharvested"]["delta nt2"]], ["\u0394N ($r_d=0.5$)", "\u0394N ($r_d=0$)", "\u0394N ($r_d=-0.5$)"],
            ["blue", "green", "red"], [0.7, -0.11])

    plt.gcf().text(0.5, 0.03, "where:\n$r_d$=[various]     $K$={}     $T$={}\n$Q$={}     $E$={}     $S$={}     $N_0$={}"
                   .format(K, T, Q, E, S, N_0), fontsize=12, ha="center")

    figure.tight_layout(pad=3)
    plt.subplots_adjust(left=None, bottom=0.2, right=0.9, top=None, wspace=None, hspace=None)

# issue 2 - fixed harvesting
elif ISSUE == 2:
    figure, subp = plt.subplots(num=2, nrows=1, ncols=2, figsize=(15, 6))
    figure.canvas.set_window_title("Figure 2: LHM under harvesting")
    plt.suptitle("Population of Fish over {} years under different Harvesting Methods".format(T), fontsize=14)

    plotter(subp, True, [0], "Population Under Fixed-quota Harvesting", plots["t"]["label"], "Population",
            [plots["fq"]["values"], plots["fq"]["actual harvest"]], ["N", "Actual Harvest"],
            ["brown", "orange"], [0.3, -0.11])

    #plotter(subp, True, [1], "Population Under Fixed-effort Harvesting", plots["t"]["label"], "Population",
     #       [plots["fe"]["values"], plots["fe"]["effort line"]], ["N", "Effort Line"],
     #       [plots["unharvested"]["colour"], "red"], [0.7, -0.11])

    subp[1].plot(plots["unharvested"]["values"], plots["unharvested"]["delta nt"])
    subp[1].plot([Q] * K)

    plt.gcf().text(0.5, 0.03, "where:\n$r_d$={}     $K$={}     $T$={}\n$Q$={}     $E$={}     $S$={}     $N_0$={}"
                   .format(RD, K, T, Q, E, S, N_0), fontsize=12, ha="center")

    figure.tight_layout(pad=3)
    plt.subplots_adjust(left=None, bottom=0.2, right=0.9, top=None, wspace=None, hspace=None)

# issue 3 - stochastic harvesting
elif ISSUE == 3:
    figure, subp = plt.subplots(num=2, nrows=1, ncols=1, figsize=(10, 8))
    figure.canvas.set_window_title("Figure 3: LHM with Stochasticity")
    plt.suptitle("Population of Fish over {} years with stochasticity".format(T), fontsize=14)

    # plot data
    plotter(subp, False, 0, "Harvesting With Stochasticity", plots["t"]["label"], "Population Harvest",
            [plots["fq_s"]["values"], plots["fe_s"]["values"]],
            [plots["fq_s"]["label"], plots["fe_s"]["label"]], [plots["fq"]["colour"], plots["fe"]["colour"]],
            [0.5, -0.08])

    # display constant values below plot
    plt.gcf().text(0.5, 0.03, "where:\n$r_d$={}     $K$={}     $T$={}     $Q$={}     $E$={}     $S$={}"
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
