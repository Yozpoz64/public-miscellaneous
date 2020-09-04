# ENVSCI 203 Population Growth Model
# Created for assignment 3
#
# Created by Samuel Kolston
# Created on: 290820
# Last edited: 040920 154900
#
# TO DO
# -add function for plotting/subplotting

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
SHOW_STATUS = True
SHOW_PLOTS = False


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

# add time and carry capacity to lists for plotting
for time in range(T + 1):
    plots["k"]["values"].append(K)
    plots["t"]["values"].append(time)
    plots["q"]["values"].append(Q)


# function that performs the base logistic calculation
def gen_log(nt, growth_rate, carry_cap):
    return nt + growth_rate * nt * (1 - nt / carry_cap)


# function that performs the base logistic calculation with stochasticity
def stochastic_log(nt, growth_rate, carry_cap, sd):
    return nt + (growth_rate + growth_rate * sd) * nt * (1 - nt / carry_cap)


# function that checks if harvest is absolute
def max_0(harvest, harvest_list):
    if harvest >= 0:
        harvest_list.append(harvest)
    else:
        harvest_list.append(0)


# function that calculates S * D for stochasticity
def randbetween(s_value):
    return s_value * (random.randint(-1000, 1000) / 1000)


# calculates actual harvest
def actual_harvest(harvest, state, actharvest_list):
    if harvest > state:
        actharvest_list.append(state)
    else:
        actharvest_list.append(harvest)


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

# FUNCTION FOR PLOTTING?
if SHOW_PLOTS:
    # LHM plots
    figure, subp = plt.subplots(num=1, nrows=2, ncols=2, figsize=(12, 10))
    figure.canvas.set_window_title("Figure 1: LHM")
    plt.suptitle("Population of Fish over {} years".format(T), fontsize=14)

    # top left subplot
    subp[0, 0].set_ylabel("Population")
    subp[0, 0].set_title(plots["unharvested"]["label"])
    subp[0, 0].plot(plots["unharvested"]["values"], label="N", color=plots["unharvested"]["colour"])
    subp[0, 0].plot(plots["unharvested"]["delta nt"], label="Growth rate", color="red")
    subp[0, 0].legend(ncol=2, bbox_to_anchor=(0.5, -0.15), loc="upper center")
    subp[0, 0].set_xlabel(plots["t"]["label"])

    # top right subplot
    subp[0, 1].set_ylabel("Population")
    subp[0, 1].set_title("Harvested")
    subp[0, 1].plot(plots["fq"]["values"], label=plots["fq"]["label"], color=plots["fq"]["colour"])
    subp[0, 1].plot(plots["fe"]["values"], label=plots["fe"]["label"], color=plots["fe"]["colour"])
    subp[0, 1].legend(ncol=2, bbox_to_anchor=(0.5, -0.15), loc="upper center")
    subp[0, 1].set_xlabel(plots["t"]["label"])

    # bottom left subplot
    subp[1, 0].set_ylabel("Population Harvest")
    subp[1, 0].set_title("Quota vs Actual Harvest (Fixed-quota)")
    subp[1, 0].plot(plots["q"]["values"], label="Quota", color="black")
    subp[1, 0].plot(plots["fq"]["actual harvest"], label="Actual Harvest", color="brown")
    subp[1, 0].legend(ncol=2, bbox_to_anchor=(0.5, -0.15), loc="upper center")
    subp[1, 0].set_xlabel(plots["t"]["label"])

    # bottom right subplot
    subp[1, 1].set_ylabel("Population Harvest")
    subp[1, 1].set_title("Fixed-effort Actual Harvest")
    subp[1, 1].plot(plots["fe"]["actual harvest"], label="Actual Harvest")
    subp[1, 1].legend(ncol=2, bbox_to_anchor=(0.5, -0.15), loc="upper center")
    subp[1, 1].set_xlabel(plots["t"]["label"])

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

    subp.set_ylabel("Population")
    subp.set_title("Harvesting With Stochasticity")
    subp.plot(plots["fq_s"]["values"], label=plots["fq_s"]["label"], color=plots["fq"]["colour"])
    subp.plot(plots["fe_s"]["values"], label=plots["fe_s"]["label"], color=plots["fe"]["colour"])
    subp.legend(ncol=2, bbox_to_anchor=(0.5, -0.08), loc="upper center")
    subp.set_xlabel(plots["t"]["label"])

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
