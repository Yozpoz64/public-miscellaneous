# SLOPE CALCULATOR (v2)
# Calculates slope for faux raster cells using method given in GISCI242
# Created by Samuel Kolston
# Last edited: 200420 1139
#
# TO DO:
# -input method is really crappy. need to implement a tkinter gui with text boxes
# -bad coding. need to figure out algorithm to find neighbour amounts and directions
# -calc aspect?
final_slopes = []
values = []
locations = ["1a", "1b", "1c", "2a", "2b", "2c", "3a", "3b", "3c"]


def calc(cell_to_calc, neighbour_cell, location):
    if location == 0:
        mod = 100
    elif location == 1:
        mod = 141.42
    calculation = round((abs((values[cell_to_calc][0] - values[neighbour_cell][0]) / mod)), 2) * 100
    return int(calculation)

print("     a  b  c")
print(" 1 |  |  |  | \n 2 |  |  |  | \n 3 |  |  |  | \n")

for count in range(len(locations)):
    cell_value = int(input("Cell {} value: ".format(locations[count])))
    values.append([cell_value, locations[count]])

for cell in range(len(locations)):
    if values[cell][1] == "1a":
        final_slopes.append(max(calc(cell, 1, 0), calc(cell, 3, 0), calc(cell, 4, 1)))
    elif values[cell][1] == "1b":
        final_slopes.append(max(calc(cell, 0, 0), calc(cell, 2, 0), calc(cell, 4, 0), calc(cell, 3, 1),
                                calc(cell, 5, 1)))
    elif values[cell][1] == "1c":
        final_slopes.append(max(calc(cell, 1, 0), calc(cell, 5, 0), calc(cell, 4, 1)))
    elif values[cell][1] == "2a":
        final_slopes.append(max(calc(cell, 0, 0), calc(cell, 4, 0), calc(cell, 6, 0), calc(cell, 1, 1),
                                calc(cell, 7, 1)))
    elif values[cell][1] == "2b":
        final_slopes.append(max(calc(cell, 0, 1), calc(cell, 1, 0), calc(cell, 2, 1), calc(cell, 3, 0),
                                calc(cell, 5, 0), calc(cell, 6, 1), calc(cell, 7, 0), calc(cell, 8, 1)))
    elif values[cell][1] == "2c":
        final_slopes.append(max(calc(cell, 2, 0), calc(cell, 4, 0), calc(cell, 8, 0), calc(cell, 1, 1),
                                calc(cell, 7, 1)))
    elif values[cell][1] == "3a":
        final_slopes.append(max(calc(cell, 3, 0), calc(cell, 7, 0), calc(cell, 4, 1)))
    elif values[cell][1] == "3b":
        final_slopes.append(max(calc(cell, 4, 0), calc(cell, 6, 0), calc(cell, 8, 0), calc(cell, 3, 1),
                                calc(cell, 5, 1)))
    elif values[cell][1] == "3c":
        final_slopes.append(max(calc(cell, 5, 0), calc(cell, 7, 0), calc(cell, 4, 1)))

print("\n {0}% {1}% {2}% \n {3}% {4}% {5}% \n {6}% {7}% {8}%".format(*final_slopes))
