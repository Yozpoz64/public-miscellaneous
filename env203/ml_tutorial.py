import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_table = pd.read_excel('Clark.xlsx')

independant_vars = ['Rain24', 'Rain48', 'Rain72', 'RainWA', 'Wdirection', 'Wspeed', 'SolarHours']
df_dict = {}
std_dict = {}


def std_calc(df):
    return (df - np.min(df)) / (np.max(df) - np.min(df))

'''
for measurement in independant_vars:
    df_dict.update({measurement: pd.DataFrame(data_table[measurement])})
    std_dict.update({'{}_std'.format(measurement): (df_dict[measurement] - np.min(df_dict[measurement])) /
                                                   (np.max(df_dict[measurement]) - np.min(df_dict[measurement]))})

factor_data = np.array([df_dict[independant_vars[0]], df_dict[independant_vars[1]], df_dict[independant_vars[2]],
                        df_dict[independant_vars[3]], df_dict[independant_vars[4]], df_dict[independant_vars[5]],
                        df_dict[independant_vars[6]]])
'''


entero = pd.DataFrame(data_table['Entero'])

print(df_dict)



plt.show()
