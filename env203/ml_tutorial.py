import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dt = pd.read_excel('Clark.xlsx') # dataframe creation not provided


def std_calc(df):
    return (df - np.min(df)) / (np.max(df) - np.min(df))


'''
independant_vars = ['Rain24', 'Rain48', 'Rain72', 'RainWA', 'Wdirection', 'Wspeed', 'SolarHours']
df_dict = {}
std_dict = {}

for measurement in independant_vars:
    df_dict.update({measurement: pd.DataFrame(data_table[measurement])})
    std_dict.update({'{}_std'.format(measurement): (df_dict[measurement] - np.min(df_dict[measurement])) /
                                                   (np.max(df_dict[measurement]) - np.min(df_dict[measurement]))})

factor_data = np.array([df_dict[independant_vars[0]], df_dict[independant_vars[1]], df_dict[independant_vars[2]],
                        df_dict[independant_vars[3]], df_dict[independant_vars[4]], df_dict[independant_vars[5]],
                        df_dict[independant_vars[6]]])
'''

rain24 = pd.DataFrame(dt['Rain24'])
rain48 = pd.DataFrame(dt['Rain48'])
rain72 = pd.DataFrame(dt['Rain72'])
rainwa = pd.DataFrame(dt['RainWA'])
wdirection = pd.DataFrame(dt['Wdirection'])
wspeed = pd.DataFrame(dt['Wspeed'])
solarhours = pd.DataFrame(dt['SolarHours'])

rain24_std = std_calc(rain24)
rain48_std = std_calc(rain48)
rain72_std = std_calc(rain72)
rainwa_std = std_calc(rainwa)
wdirection_std = std_calc(wdirection)
wspeed_std = std_calc(wspeed)
solarhours_std = std_calc(solarhours)

factor_data = np.array([rain24_std, rain48_std, rain72_std, rainwa_std, wdirection_std, wspeed_std, wdirection_std,
                        solarhours_std], dtype=float)
input_data = factor_data.T

indicies = np.random.permutation(len(rain24_std))
n_training_samples = round(len(rain24_std) * 0.7)
trainset_data = input_data[indicies[-n_training_samples:]]
# trainset_labels = water_label[indicies[-n_training_samples:]] water_label not provided
