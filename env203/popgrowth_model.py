# ENVSCI 203 Population Growth Model
# created for assignment 3
#   -excel is a better program for this assignment imo
#   -just created for fun and to understand the model better
#
# Created by Samuel Kolston
# Created on: 290820
# Last edited: 300820

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


RD = 0.5
K = 2000
T = 50
N_0 = 1
Q = 250
E = 0.5
TYPE = 1

plots = \
    {
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
        "output":
            {
                "label": "Population",
                "colour": "blue",
                "values": [N_0],
            },
        "actual harvest":
            {
                "label": "Actual Harvest",
                "colour": "green",
                "values": [],
            }
    }

calc_plots = \
    {
        "unharvested":
            {
                "label": "Unharvested Population",
                "colour": "blue",
                "values": [N_0]
            },
        "harvested_fq":
            {
                "label": "Fixed-quota Harvested Population",
                "colour": "purple",
                "values": [K]
            },
        "harvested_fe":
            {
                "label": "Fixed-effort Harvested Population",
                "colour": "green",
                "values": [],
                "effort line": [],
                "actual harvest": []
            }
    }

for time in range(T + 1):
    plots["k"]["values"].append(K)
    plots["t"]["values"].append(time)


def logistic_harvesting(growth_rate, carry_cap, years, quota, effort):
    for i in range(years):
        calc_plots["unharvested"]["values"].append(calc_plots["unharvested"]["values"][-1] + growth_rate *
                                                   calc_plots["unharvested"]["values"][-1] *
                                                   (1 - calc_plots["unharvested"]["values"][-1] / carry_cap))

        nt_1_q = calc_plots["harvested_fq"]["values"][-1] + growth_rate * calc_plots["harvested_fq"]["values"][-1]\
                                                * (1 - calc_plots["harvested_fq"]["values"][-1] / carry_cap) - quota
        if nt_1_q >= 0:
            calc_plots["harvested_fq"]["values"].append(nt_1_q)
        else:
            calc_plots["harvested_fq"]["values"].append(0)

        nt_1_e = n_t + growth_rate * n_t * (1 - n_t / carry_cap) - effort * n_t


'''
def unharvested(growth_rate, carry_cap, years):
    for i in range(years):
        n_t = plots["output"]["values"][-1]
        plots["output"]["values"].append(n_t + growth_rate * n_t * (1 - n_t / carry_cap))


def harvested_fq(growth_rate, carry_cap, years, quota):
    for i in range(years):
        n_t = plots["output"]["values"][-1]
        n_t_1 = n_t + growth_rate * n_t * (1 - n_t / carry_cap) - quota
        if n_t_1 >= 0:
            plots["output"]["values"].append(n_t_1)
        else:
            plots["output"]["values"].append(0)


def harvested_fe(growth_rate, carry_cap, years, effort):
    for i in range(years):
        n_t = plots["output"]["values"][-1]
        n_t_1 = n_t + growth_rate * n_t * (1 - n_t / carry_cap) - effort * n_t
        if n_t_1 >= 0:
            plots["output"]["values"].append(n_t_1)
        else:
            plots["output"]["values"].append(0)
        if len(plots["output"]["values"]) > 1:
            plots["actual harvest"]["values"].append(effort * n_t)


def stochastic():
    return


if TYPE == 0:
    unharvested(RD, K, T)
elif TYPE == 1:
    harvested_fq(RD, K, T, Q)
elif TYPE == 2:
    harvested_fe(RD, K, T, E)
'''
'''
figure(num=None, figsize=(13, 7), dpi=80, facecolor='w', edgecolor='k')
plt.xlabel(plots["t"]["label"])
plt.ylabel(plots["output"]["label"])
plt.title("{} over {} Year(s)".format(plots["output"]["label"], T))

plt.plot(plots["t"]["values"], plots["output"]["values"], label=plots["output"]["label"], color=plots["output"]["colour"])
plt.plot(plots["t"]["values"], plots["k"]["values"], label=plots["k"]["label"], color=plots["k"]["colour"])

plt.legend(ncol=1, bbox_to_anchor=(1.04, 1), loc="upper left")
plt.subplots_adjust(left=None, bottom=None, right=0.8, top=None, wspace=None, hspace=None)
plt.show()
'''
logistic_harvesting(RD, K, T, Q, E)
figure, subp = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
'''
subp[0].set_xlabel(plots["t"]["label"])
subp[0].set_ylabel(plots["output"]["label"])
subp[0].set_title("{} over {} Year(s)".format(plots["output"]["label"], T))
subp[0].plot(plots["t"]["values"], plots["output"]["values"], label=plots["output"]["label"], color=plots["output"]["colour"])
subp[0].plot(plots["t"]["values"], plots["k"]["values"], label=plots["k"]["label"], color=plots["k"]["colour"])
subp[0].legend(ncol=2, bbox_to_anchor=(0.5, -0.15), loc="upper center")
'''

subp[0].plot(calc_plots["unharvested"]["values"])
subp[0].plot(calc_plots["harvested_fq"]["values"])
figure.tight_layout(pad=3)
plt.subplots_adjust(left=None, bottom=0.2, right=0.9, top=None, wspace=None, hspace=None)

print(plots["actual harvest"]["values"])
print(plots["output"]["values"])

plt.show()
