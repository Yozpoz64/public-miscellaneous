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
TYPE = 0

output = [N_0]

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
                "values": [N_0]
            }
    }

for time in range(T + 1):
    plots["k"]["values"].append(K)
    plots["t"]["values"].append(time)
    #plots["q"]["values"].append(Q)


def unharvested(growth_rate, carry_cap, years):
    for i in range(years):
        n_t = plots["output"]["values"][-1]
        plots["output"]["values"].append(n_t + growth_rate * n_t * (1 - n_t / carry_cap))


def harvested(growth_rate, carry_cap, years, quota):
    for i in range(years):
        n_t = plots["output"]["values"][-1]
        n_t_1 = n_t + growth_rate * n_t * (1 - n_t / carry_cap) - quota
        if n_t_1 >= 0:
            plots["output"]["values"].append(n_t_1)
        else:
            plots["output"]["values"].append(0)


def stochastic():
    return


if TYPE == 0:
    unharvested(RD, K, T)
elif TYPE == 1:
    harvested(RD, K, T, Q)


figure(num=None, figsize=(13, 7), dpi=80, facecolor='w', edgecolor='k')
plt.xlabel(plots["t"]["label"])
plt.ylabel(plots["output"]["label"])
plt.title('Population over {} Year(s)'.format(T))

plt.plot(plots["t"]["values"], plots["output"]["values"], label=plots["output"]["label"], color=plots["output"]["colour"])
plt.plot(plots["t"]["values"], plots["k"]["values"], label=plots["k"]["label"], color=plots["k"]["colour"])

plt.legend(ncol=1, bbox_to_anchor=(1.04, 1), loc="upper left")
plt.subplots_adjust(left=None, bottom=None, right=0.8, top=None, wspace=None, hspace=None)
plt.show()

print(plots["output"]["values"])
