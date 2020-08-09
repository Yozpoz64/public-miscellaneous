import pylab as plt
import numpy as np

# constants
C = 0.1                 # level of erosion
FEEDBACK = "negative"   # changes equation used
YEARS = 10000              # n years to run
PLOT_TYPE = 1           # 0 plots origin and last n, 1 plots all n
SHOW_STATUS = True

# lists for sites and origin elevation profile
x_site = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
origin = [1000, 970, 950, 920, 830, 760, 605, 585, 550, 520, 400, 300, 225, 150, 100]
# origin = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]

# nest origin profile into results for origin plotting
model_results = [origin]

years = 1000
feedback = "positive"


prev_year = origin
for time in range(years):
    current_year = [origin[0]]
    for index in range(len(x_site) - 1):
        if feedback == "positive":
            current_year.append(round(prev_year[index + 1] - C * (prev_year[index] - prev_year[index + 1])))
    model_results.append(current_year)
    prev_year = current_year
    plt.plot(x_site, model_results[time], label="Year {}".format(time))
    plt.draw()
    plt.pause(0.01)

plt.show()
