# SLOPE CALCULATOR
# Calculates slope for faux raster cells using method given in GISCI242
# Created by Samuel Kolston
# Last edited: 200420 0126
#
# Really simple, things to improve:
# -input method is really crappy. need to implement a tkinter gui with text boxes
# -need to think about algorithm for doing all cells at once
ADJ = 100
DIAG = 141.42  # rounded result of 100 * sqrt(2)
num_cells = -1
cell_slopes = []

cell_value = int(input("Value of cell: "))

while num_cells < 0:
    num_cells = int(input("Number of neighbouring cells (must be greater than 0): "))

print("\nEnter cell values one by one and whether they are adjacent (a) or diagonal (d) from main cell\n"
      "Seperate with a period\neg. '61.d'\n")

for count in range(num_cells):
    current_cell = input("Input cell and relative location: ").split(".")
    if current_cell[1] == "a":
        cell_slopes.append(round(abs(((cell_value - int(current_cell[0])) / ADJ)), 2))
    elif current_cell[1] == "d":
        cell_slopes.append(round(abs(((cell_value - int(current_cell[0])) / DIAG)), 2))

print("\nSlope for cell {}: {}%".format(cell_value, round(max(cell_slopes) * 100)))

