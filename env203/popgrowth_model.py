# ENVSCI 203 Population Growth Model
# created for assignment 3
#   -excel is a better program for this assignment imo
#   -just created for fun and to understand the model better
#
# Created by Samuel Kolston
# Created on: 290820
# Last edited: 300820

import matplotlib.pyplot as plt


RD = 0.5
K = 2000
T = 50
N_0 = 1
Q = 250
E = 0.5

plots = \
    {
        "unharvested":
            {
                "label": "Unharvested",
                "colour": "blue",
                "values": [N_0]
            },
        "harvested_fq":
            {
                "label": "Fixed-quota",
                "colour": "pink",
                "values": [K],
                "actual harvest": []
            },
        "harvested_fe":
            {
                "label": "Fixed-effort",
                "colour": "green",
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

for time in range(T + 1):
    plots["k"]["values"].append(K)
    plots["t"]["values"].append(time)


def logistic_harvesting(growth_rate, carry_cap, years, quota, effort):
    for i in range(years):
        # not harvesting
        plots["unharvested"]["values"].append(plots["unharvested"]["values"][-1] + growth_rate *
                                              plots["unharvested"]["values"][-1] *
                                              (1 - plots["unharvested"]["values"][-1] / carry_cap))

        # harvesting under fixed quota
        nt_1_q = plots["harvested_fq"]["values"][-1] + growth_rate * plots["harvested_fq"]["values"][-1] \
                 * (1 - plots["harvested_fq"]["values"][-1] / carry_cap) - quota
        if nt_1_q >= 0:
            plots["harvested_fq"]["values"].append(nt_1_q)
        else:
            plots["harvested_fq"]["values"].append(0)

        # harvesting under fixed effort
        nt_1_e = plots["harvested_fe"]["values"][-1] + growth_rate * plots["harvested_fe"]["values"][-1] * \
                 (1 - plots["harvested_fe"]["values"][-1] / carry_cap) - effort * \
                 plots["harvested_fe"]["values"][-1]
        if nt_1_e >= 0:
            plots["harvested_fe"]["values"].append(nt_1_e)
        else:
            plots["harvested_fe"]["values"].append(0)
        plots["harvested_fe"]["actual harvest"].append(effort * nt_1_e)  # THIS DOES NOT WORK - needs the first value
        plots["harvested_fe"]["effort line"].append(effort * plots["unharvested"]["values"][-1])


logistic_harvesting(RD, K, T, Q, E)

figure, subp = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
plt.suptitle("Population of ____ over {} years".format(T), fontsize=14)

subp[0].set_ylabel("Population")
subp[0].set_title("Unharvested")
subp[0].plot(plots["unharvested"]["values"], label=plots["unharvested"]["label"], color=plots["unharvested"]["colour"])
subp[0].legend(ncol=2, bbox_to_anchor=(0.5, -0.15), loc="upper center")
subp[0].set_xlabel(plots["t"]["label"])

subp[1].set_title("Harvested")
subp[1].plot(plots["harvested_fq"]["values"], label=plots["harvested_fq"]["label"], color=plots["harvested_fq"]["colour"])
subp[1].plot(plots["harvested_fe"]["values"], label=plots["harvested_fe"]["label"], color=plots["harvested_fe"]["colour"])
subp[1].legend(ncol=2, bbox_to_anchor=(0.5, -0.15), loc="upper center")
subp[1].set_xlabel(plots["t"]["label"])

figure.tight_layout(pad=3)
plt.subplots_adjust(left=None, bottom=0.2, right=0.9, top=None, wspace=None, hspace=None)

print(plots["harvested_fq"]["values"])
print(plots["harvested_fe"]["values"])
print(plots["harvested_fe"]["actual harvest"])
print(plots["harvested_fe"]["effort line"])


plt.show()
