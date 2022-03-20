import os
import home
import graph
import view

# Create pygame window
os.environ['SDL'] = '25012002'

# Run home screen to input file path
path_input = home.InputPage(name='Robot Path Finding', size=(0, 0, 800, 600), title='Input file:')
option, path = path_input.run()

# User entered a file path, then run the main program
if option == 1:
   print('User enters file path:', path)
   try:
       view_map = graph.Map()
       view_size, view_grid = view_map.load(path)
       view = view.View(view_map, view_grid, view_size)
       view.run()
   except Exception as e:
      print(str(e))
      exit()

# User clicked exit button
elif option == -1:
   exit()