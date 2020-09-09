import pandas as pd
import matplotlib.pyplot as plt

data_table = pd.read_excel('Clark.xlsx')

rain24 = pd.DataFrame(data_table['Rain24'])

plt.plot(rain24)

plt.show()
