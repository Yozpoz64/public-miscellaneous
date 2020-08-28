# ENVSCI 203 Population Growth Model
# created for assignment 3
#   -excel is a better program for this assignment imo
#   -just created for fun and to understand the model better
#
# Created by Samuel Kolston
# Created on: 290820
# Last edited: 290820

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


RD = 0.5
K = 2000
T = 50
N_0 = 1

output = []
t_list = []
k_list = []

for time in range(T + 1):
    t_list.append(time)
    k_list.append(K)


def unharvested(growth_rate, carry_cap, years, origin):
    output.append(origin)
    for i in range(years):
        n_t = output[-1]
        output.append(n_t + growth_rate * n_t * (1 - n_t / carry_cap))


unharvested(RD, K, T, N_0)

figure(num=None, figsize=(13, 7), dpi=80, facecolor='w', edgecolor='k')

plt.xlabel('Year')
plt.ylabel('Population (n)')
plt.title('Population without Harvesting over {} Year(s)'.format(T))
plt.plot(t_list, output, label="Population")
plt.plot(t_list, k_list, label="Carrying Capacity")
plt.legend(ncol=1, bbox_to_anchor=(1.04, 1), loc="upper left")
plt.subplots_adjust(left=None, bottom=None, right=0.8, top=None, wspace=None, hspace=None)
plt.show()


print(t_list)
print(output)
