import os
import hue
files = os.listdir() 
main = hue.Window(files)
main.run()
