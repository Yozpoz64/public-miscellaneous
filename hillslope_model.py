# ENVSCI 203
# my interpretation of the feedback model used in ENV203 assignment 2
# implemented in python instead of Excel to make it easier for excessive
#   temporal analysis (50+ years)
#
# Created by: Samuel Kolston
# Created on: 080820
# Last edited: 080820

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.pyplot import figure

figure(num=None, figsize=(10, 7), dpi=80, facecolor='w', edgecolor='k')

C = 0.1
FEEDBACK = "positive"

x_site = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
origin = [1000, 970, 950, 920, 830, 760, 605, 585, 550, 520, 400, 300, 225, 150, 100]

model_results = [origin]

years = int(input("Number of years to model: "))


def positive_fb(origin, years, feedback):
    prev_year = origin
    for i in range(years):
        tmp_list = [origin[0]]
        for x in range(14):
            if feedback == "positive":
                tmp_list.append(round(prev_year[x+1] - C * (prev_year[x] - prev_year[x+1])))
            elif feedback == "negative":
                try:
                    tmp_list.append(round(prev_year[x+1] - C * (prev_year[x+1] - prev_year[x+2])))
                except IndexError:
                    tmp_list.append(round(prev_year[x+1] - C * (prev_year[x+1] - 0)))
        model_results.append(tmp_list)
        prev_year = tmp_list


positive_fb(origin, years, FEEDBACK)

for i in range(len(model_results)):
    plt.plot(x_site, model_results[i], label="Year {}".format(i))


fontP = FontProperties()
fontP.set_size('small')
plt.legend(ncol=2, bbox_to_anchor=(1.04, 1), loc="upper left", prop=fontP)
plt.xticks(np.arange(min(x_site), max(x_site)+1, 1.0))
plt.subplots_adjust(left=None, bottom=None, right=0.7, top=None, wspace=None, hspace=None)
plt.xlabel('Site')
plt.ylabel('Elevation (m)')
plt.title('Hillslope Profile Modelled under {} Feedback Conditions over {} Year(s)'.format(FEEDBACK.title(), years))

plt.show()
