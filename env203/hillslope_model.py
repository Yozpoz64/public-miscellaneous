# ENVSCI 203 hillslope_model.py
# my interpretation of the feedback model used in ENV203 assignment 2
# implemented in python instead of Excel to make it easier for excessive
#   temporal analysis (50+ years)
#
# requires matplotlib and dependencies "pip install matplotlib"
# gets slightly different results from Excel. (+/- 8%)
#   -doesnt appear to be a rounding issue
#   -try rebuilding the model without lists etc.
#
# Created by Samuel Kolston
# Created on: 080820
# Last edited: 110820

# modules
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure
import time
import random

# begin time elapsed
start_time = time.time()

# constants
C = 0.1                 # level of erosion
FEEDBACK = "positive"   # changes equation used
YEARS = 100             # n years to run
PLOT_TYPE = 0           # 1 plots origin and last n, 0 plots all n
SHOW_STATUS = True      # show progress in console
DIV_FACTOR = 100        # frequency of displaying process updates
SHOW_LIVE = True        # draw the series one by one

# create matplotlib fig
figure(num=None, figsize=(10, 7), dpi=80, facecolor='w', edgecolor='k')

# lists for sites and origin elevation profile
# x_site = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
x_site = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
origin = [1000, 970, 950, 920, 830, 760, 605, 585, 550, 520, 400, 300, 225, 150, 100]
# origin = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
# origin = [1000, 985, 970, 960, 950, 935, 920, 875, 830, 795, 760, 683, 605, 595, 585, 568, 550, 535, 520, 460, 400,
 #         350, 300, 263, 225, 188, 150, 125, 100, 50]


# nest origin profile into results for origin plotting
model_results = [origin]


# status function
def show_status(index, limit, div_factor, action):
    if index % div_factor == 0:
        return "{} {} of {}".format(action, index, limit)
    else:
        return False


# modelling function
def fb_model(origin, years, feedback):
    prev_year = origin
    for time in range(years):
        current_year = [origin[0]]
        print(current_year)
        for index in range(len(x_site) - 1):
            if feedback == "positive":
                current_year.append(round(prev_year[index+1] - C * (prev_year[index] - prev_year[index+1])))
            elif feedback == "negative":
                try:
                    current_year.append(round(prev_year[index+1] - C * (prev_year[index+1] - prev_year[index+2])))
                except IndexError:
                    current_year.append(round(prev_year[index+1] - C * (prev_year[index+1] - 0)))

        model_results.append(current_year)
        prev_year = current_year
        if SHOW_STATUS:
            status_display = show_status(time, YEARS, DIV_FACTOR, "modelled")
            if status_display:
                print(status_display)


# call modelling function using constants
fb_model(origin, YEARS, FEEDBACK)


# choose how to plot based on constant
if PLOT_TYPE == 0:
    for i in range(len(model_results)):
        plt.plot(x_site, model_results[i], label="Year {}".format(i))
        if SHOW_LIVE:
            plt.draw()
            plt.pause(0.01)
        if SHOW_STATUS:
            status_display = show_status(i, len(model_results), DIV_FACTOR, "plotted")
            if status_display:
                print(status_display)
elif PLOT_TYPE == 1:
    plt.plot(x_site, model_results[0], label="Year 1")
    '''
    plt.plot(x_site, model_results[len(model_results) - 999901], label="Year {}".format(len(model_results) - 999901))
    plt.plot(x_site, model_results[len(model_results) - 999001], label="Year {}".format(len(model_results) - 999001))
    plt.plot(x_site, model_results[len(model_results) - 990001], label="Year {}".format(len(model_results) - 990001))
    plt.plot(x_site, model_results[len(model_results) - 900001], label="Year {}".format(len(model_results) - 900001)
    '''
    plt.plot(x_site, model_results[len(model_results) - 1], label="Year {}".format(len(model_results) - 1))


# after lines are plotted, format plot with titles etc.
plt.legend(ncol=2, bbox_to_anchor=(1.04, 1), loc="upper left")
plt.xticks(np.arange(min(x_site), max(x_site)+1, 1.0))
plt.subplots_adjust(left=None, bottom=None, right=0.7, top=None, wspace=None, hspace=None)
plt.xlabel('Site')
plt.ylabel('Elevation (m)')
plt.title('Hillslope Profile Modelled under {} Feedback Conditions \nover {} Year(s)'.format(FEEDBACK.title(), YEARS))

# display final modelling status info
if SHOW_STATUS:
    elapsed = round(time.time() - start_time, 4)
    print("\n{} years of hillslope profiles modelled and plotted in {} seconds".format(YEARS, elapsed))
    print("final profile:", model_results[-1])

# finish plot display (hang)
plt.show()
