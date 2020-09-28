# ENVSCI 203 Population Growth Model
# Created for assignment 3
#
# Created by Samuel Kolston
# Created on: 290820
# Last edited: 230920 1306
#

# modules
import matplotlib.pyplot as plt
import random

# constants
RD = 0.5
K = 2000
T = 100000
N_0 = 2000
Q = 400
E = 0.499
# constants for debugging
SHOW_STATUS = False
ISSUE = 2  # changes plot output for assignment (0 for old SHOW_PLOT)
FIGURE = 4


# dict for model values and associated plot preferences
plots = \
    {
        "unharvested":
            {
                "label": "Unharvested",
                "colour": "blue",
                "values": [N_0], # needs to change to 1 for harvesting
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
                "values": [N_0],
                "actual harvest": []
            },
        "fe":
            {
                "label": "Fixed-effort",
                "colour": "green",
                "values": [N_0],
                "effort line": [0],
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
                "label": "Years (t)",
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
    tmp.set_ylim(0 - 100, K + 100)
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


# calculates actual harvest if applicable
for i in range(T + 1):
    actual_harvest(plots["fq"]["values"][i], Q, plots["fq"]["actual harvest"])
    actual_harvest(plots["fe"]["values"][i], E * plots["fe"]["values"][i], plots["fe"]["actual harvest"])

# issue 1 - unharvested
if ISSUE == 1:
    if FIGURE == 1:
        figure, subp = plt.subplots(num=2, nrows=1, ncols=2, figsize=(15, 6))
        figure.canvas.set_window_title("Figure 1: LHM")
        plt.suptitle("Population of Fish over {} years at various Rates of Growth".format(T), fontsize=14)

        plotter(subp, True, [0], "Unharvested Population Growth", plots["t"]["label"], "Population (N)",
                [plots["unharvested"]["values"], plots["unharvested"]["values rd1"], plots["unharvested"]["values rd2"], plots["k"]["values"]], ["N ($r_d=0.5$)", "N ($r_d=0$)", "N ($r_d=-0.5$)", "K"],
                ["blue", "green", "red", "brown"], [0.3, -0.11])

        plotter(subp, True, [1], "Unharvested Change in Population", plots["t"]["label"], "Change in Population (\u0394N)",
                [plots["unharvested"]["delta nt"], plots["unharvested"]["delta nt1"], plots["unharvested"]["delta nt2"]], ["\u0394N ($r_d=0.5$)", "\u0394N ($r_d=0$)", "\u0394N ($r_d=-0.5$)"],
                ["blue", "green", "red"], [0.7, -0.11])

        plt.gcf().text(0.5, 0.03, "where:\n$r_d$=[various]     $K$={}     $T$={}\n$Q$={}     $N_0$={}"
                       .format(K, T, Q, N_0), fontsize=12, ha="center")

        figure.tight_layout(pad=3)
        plt.subplots_adjust(left=None, bottom=0.2, right=0.9, top=None, wspace=None, hspace=None)
    elif FIGURE == 2:
        figure, subp1 = plt.subplots(num=3, nrows=1, ncols=1, figsize=(9, 6))
        #plotter(subp1, False, [0], "Change in Population vs Population Size", plots["t"]["label"], "Population (N)",
        #        [plots["unharvested"]["values"], plots["unharvested"]["delta nt"]], ["N", "\u0394N"], ["blue", "red"],
         #       [0.7, -0.11])
        subp1.plot(plots["unharvested"]["values"], plots["unharvested"]["delta nt"], label="Unharvested Population Dynamics")
        subp1.set_xlabel("Population (N)")
        subp1.set_ylabel("Change in Population (\u0394N)")
        subp1.legend(ncol=2, bbox_to_anchor=(0.7, -0.11), loc="upper center")
        plt.gcf().text(0.3, 0.02, "where:\n$r_d$={}    $K$={}     \n$T$={}     $N_0$={}"
                       .format(RD, K, T, N_0), fontsize=12, ha="center")
        figure.tight_layout(pad=3)
        plt.subplots_adjust(left=None, bottom=0.2, right=0.9, top=None, wspace=None, hspace=None)


# issue 2 - fixed harvesting
elif ISSUE == 2:
    if FIGURE == 3:
        figure, subp = plt.subplots(num=2, nrows=1, ncols=2, figsize=(16, 8))
        figure.canvas.set_window_title("Figure 2: LHM under harvesting")
        plt.suptitle("Population of Fish over {} years under different Harvesting Methods".format(T), fontsize=14)
        #plotter(subp, True, [0], "Population Under Fixed-quota Harvesting", plots["t"]["label"], "Population",
          #      [plots["fq"]["values"], plots["fq"]["actual harvest"]], ["N", "Actual Harvest"],
          #      ["brown", "orange"], [0.3, -0.11])
        plotter(subp, True, [0], "Population Under Harvesting", plots["t"]["label"], "Population (N)",
                [plots["fe"]["values"], plots["fq"]["values"], plots["k"]["values"]], ["N (Fixed Effort)", "N (Fixed Quota)", "K"],
                [plots["unharvested"]["colour"], "red", "brown"], [0.3, -0.11])
        plotter(subp, True, [1], "Actual Harvest", plots["t"]["label"], "Population Harvested (N)",
                [plots["fe"]["actual harvest"], plots["fq"]["actual harvest"]],
                ["Fixed Effort Actual Harvest", "Fixed Quota Actual Harvest"],
                ["green", "orange"], [0.7, -0.11])
    elif FIGURE == 4:
        figure, subp = plt.subplots(num=2, nrows=1, ncols=1, figsize=(9, 8))
        figure.canvas.set_window_title("Figure 2: LHM under harvesting")
        plotter(subp, False, [0], "", plots["t"]["label"], "Population (N)",
                [plots["fe"]["effort line"], plots["fe"]["values"]],
                ["Effort line", "N (Fixed Effort)"],
                ["pink", plots["unharvested"]["colour"]], [0.3, -0.11])
        '''
        plt.suptitle("Population of Fish over {} years under different Harvesting Methods".format(T), fontsize=14)
        subp.plot(plots["unharvested"]["values"], plots["unharvested"]["delta nt"], label="Unharvested Population Dynamics")
        subp.plot(plots["unharvested"]["values"], plots["fe"]["effort line"], label="Effort line")
        subp.set_xlabel("Population (N)")
        subp.set_ylabel("Change in Population (\u0394N)")
        subp.plot([Q] * K, label="Q")
        '''

        subp.legend(ncol=1, bbox_to_anchor=(0.7, -0.11), loc="upper center")

    plt.gcf().text(0.2, 0.03, "               where:\n$r_d$={}     $K$={}     $T$={}\n$E$={}     $N_0$={}"
                   .format(RD, K, T, E, N_0, fontsize=12, ha="center"))
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

# show figures and plots
plt.show()
