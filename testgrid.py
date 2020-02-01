"""
Test driver for grid display.
"""

from graphics import grid

grid.make(5, 5, 500, 500)

for col in range(5) :
    grid.fill_cell(0, col, grid.get_cur_color())
for row in range(5) :
    grid.fill_cell(row, 0, grid.get_next_color())
    
grid.label_cell(0, 0, "0")
grid.label_cell(0, 1, "1")
grid.label_cell(1, 0, "Longer label")

print("Click in grid to kill")

grid.wait()
