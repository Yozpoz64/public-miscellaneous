# ENVSCI 203 Population Growth Model
# created for assignment 3
#
# Created by Samuel Kolston
# Created on: 290820
# Last edited: 310820

import matplotlib.pyplot as plt

# constants
RD = 0.5
K = 2000
T = 50
N_0 = 1
Q = 250
E = 0.5

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

# add time and carry capacity to lists for plotting
for time in range(T + 1):
    plots["k"]["values"].append(K)
    plots["t"]["values"].append(time)


# function that performs the base logistic calculation
def gen_log(nt, growth_rate, carry_cap):
    return nt + growth_rate * nt * (1 - nt / carry_cap)


# runs all models using gen_log with modifiers and checks for abs values
for model in range(T):
    # unharvested calc
    nt1_unharvested = gen_log(plots["unharvested"]["values"][-1], RD, K)
    plots["unharvested"]["values"].append(nt1_unharvested)
    plots["unharvested"]["delta nt"].append(plots["unharvested"]["values"][-1] - plots["unharvested"]["values"][-2])

    # quota harvesting calc
    nt1_quota = gen_log(plots["harvested_fq"]["values"][-1], RD, K) - Q
    if nt1_quota >= 0:
        plots["harvested_fq"]["values"].append(nt1_quota)
    else:
        plots["harvested_fq"]["values"].append(0)

    # effort harvesting calc
    nt1_effort = gen_log(plots["harvested_fe"]["values"][-1], RD, K) - E * plots["harvested_fe"]["values"][-1]
    if nt1_effort >= 0:
        plots["harvested_fe"]["values"].append(nt1_effort)
    else:
        plots["harvested_fe"]["values"].append(0)
    plots["harvested_fe"]["effort line"].append(E * plots["unharvested"]["values"][-1])

for i in range(T + 1):
    # quota harvesting actual harvest calc
    if plots["harvested_fq"]["values"][i] > Q:
        plots["harvested_fq"]["actual harvest"].append(Q)
    else:
        plots["harvested_fq"]["actual harvest"].append(plots["harvested_fq"]["values"][i])

    # effort harvesting actual harvest calc
    if plots["harvested_fe"]["values"][i] > E * plots["harvested_fe"]["values"][i]:
        plots["harvested_fe"]["actual harvest"].append(E * plots["harvested_fe"]["values"][i])
    else:
        plots["harvested_fe"]["actual harvest"].append(plots["harvested_fe"]["values"][i])


# create figure
figure, subp = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
plt.suptitle("Population of ____ over {} years".format(T), fontsize=14)

# left subplot
subp[0].set_ylabel("Population")
subp[0].set_title("Unharvested")
subp[0].plot(plots["unharvested"]["values"], label=plots["unharvested"]["label"], color=plots["unharvested"]["colour"])
subp[0].legend(ncol=2, bbox_to_anchor=(0.5, -0.15), loc="upper center")
subp[0].set_xlabel(plots["t"]["label"])

# right subplot
subp[1].set_title("Harvested")
subp[1].plot(plots["harvested_fq"]["values"], label=plots["harvested_fq"]["label"], color=plots["harvested_fq"]["colour"])
subp[1].plot(plots["harvested_fe"]["values"], label=plots["harvested_fe"]["label"], color=plots["harvested_fe"]["colour"])
subp[1].legend(ncol=2, bbox_to_anchor=(0.5, -0.15), loc="upper center")
subp[1].set_xlabel(plots["t"]["label"])

# adjust both plots with spacing
figure.tight_layout(pad=3)
plt.subplots_adjust(left=None, bottom=0.2, right=0.9, top=None, wspace=None, hspace=None)

# print model output
print(plots["harvested_fq"]["values"])
print(plots["harvested_fq"]["actual harvest"])
print(plots["harvested_fe"]["values"])
print(plots["harvested_fe"]["actual harvest"])
print(plots["harvested_fe"]["effort line"])
print(plots["unharvested"]["values"])
print(plots["unharvested"]["delta nt"])

# show figure and plots
plt.show()
