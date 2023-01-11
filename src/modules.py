# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

try:
    import pygame 
    import random
    import csv
    import math
    import os
    from pygame import mixer

except ImportError:
    raise ImportError("The Unstoppable Engine couldn't import all of the necessary packages.")
  
# Pygame Initialization: #

pygame.init()

# Mixer Initialization: #

pygame.mixer.pre_init(44100, 16, 2, 4096)
mixer.init()
